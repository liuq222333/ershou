# coding:utf-8
from typing import Optional

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.cluster import KMeans
from sklearn.ensemble import HistGradientBoostingRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler

from utils._ml_common import age_series, parse_year

_PANDAS_VER = tuple(int(x) for x in pd.__version__.split(".")[:2])
_YEAR_FREQ = "YS" if _PANDAS_VER >= (2, 2) else "AS"
_GRANULARITY = {"day": "D", "month": "MS", "year": _YEAR_FREQ}
_PERIOD_FMT = {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}


def _exp_decay(age, a, b):
    return a * np.exp(-b * age)


class TrendAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if "addtime" in self.df.columns:
            self.df["addtime"] = pd.to_datetime(self.df["addtime"], errors="coerce")

    def timeseries(self, granularity: str) -> list:
        series = self._bucketed(granularity)
        if series.empty:
            return []
        rolling = series["avg_price"].rolling(window=3, min_periods=1).mean()
        return [
            {
                "period": series.index[i].strftime(_PERIOD_FMT[granularity]),
                "avg_price": round(float(series["avg_price"].iloc[i]), 2),
                "volume": int(series["volume"].iloc[i]),
                "rolling_avg_price": round(float(rolling.iloc[i]), 2),
            }
            for i in range(len(series))
        ]

    def forecast(self, horizon: int, granularity: str = "month") -> list:
        series = self._bucketed(granularity)
        if series.empty or horizon <= 0:
            return []
        prices = series["avg_price"].astype(float).tolist()
        freq = _GRANULARITY[granularity]
        fmt = _PERIOD_FMT[granularity]
        last_index = series.index[-1]
        future_index = pd.date_range(start=last_index, periods=horizon + 1, freq=freq)[1:]

        if len(prices) < 8:
            last = prices[-1]
            return [
                {
                    "period": future_index[i].strftime(fmt),
                    "forecast_price": round(float(last), 2),
                    "is_forecast": True,
                    "fallback": True,
                }
                for i in range(horizon)
            ]

        X, y = self._lag_features(prices)
        model = HistGradientBoostingRegressor(
            max_iter=200, learning_rate=0.08, random_state=42
        )
        model.fit(X, y)

        history = list(prices)
        predictions = []
        for _ in range(horizon):
            feat = self._lag_row(history)
            pred = float(model.predict(feat)[0])
            predictions.append(pred)
            history.append(pred)

        return [
            {
                "period": future_index[i].strftime(fmt),
                "forecast_price": round(predictions[i], 2),
                "is_forecast": True,
            }
            for i in range(horizon)
        ]

    def decompose(self, granularity: str = "month") -> dict:
        series = self._bucketed(granularity)
        if series.empty:
            return {"period": [], "observed": [], "trend": [], "seasonal": [], "residual": []}

        observed = series["avg_price"].astype(float)
        trend = observed.rolling(window=3, center=True, min_periods=1).mean()
        detrended = observed - trend

        if granularity == "month":
            months = series.index.month
            seasonal_map = detrended.groupby(months).mean()
            seasonal = pd.Series([seasonal_map.get(m, 0.0) for m in months], index=series.index)
        else:
            seasonal = pd.Series(np.zeros(len(series)), index=series.index)

        residual = observed - trend - seasonal
        periods = [ts.strftime(_PERIOD_FMT[granularity]) for ts in series.index]
        return {
            "period": periods,
            "observed": [round(float(v), 2) for v in observed.tolist()],
            "trend": [round(float(v), 2) for v in trend.tolist()],
            "seasonal": [round(float(v), 2) for v in seasonal.tolist()],
            "residual": [round(float(v), 2) for v in residual.tolist()],
        }

    def cluster(self, k: int = 4) -> list:
        data = self.df.copy()
        data["_age"] = age_series(data["vehicleage"])
        features = data[["discountprice", "_age", "kilometer"]].astype(float)
        mask = features.notna().all(axis=1)
        usable = data[mask].copy()
        if len(usable) < k:
            return []

        scaled = StandardScaler().fit_transform(usable[["discountprice", "_age", "kilometer"]])
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = model.fit_predict(scaled)

        centroids = pd.DataFrame(
            model.cluster_centers_, columns=["price", "age", "km"]
        )
        tags_price = self._tertile_tags(centroids["price"], ("低价", "中价", "高价"))
        tags_km = self._tertile_tags(centroids["km"], ("低里程", "中里程", "高里程"))
        tags_age = self._tertile_tags(centroids["age"], ("新车", "次新车", "老车"))

        cluster_labels = {
            i: f"{tags_price[i]}·{tags_km[i]}·{tags_age[i]}" for i in range(k)
        }

        ids = usable["id"].tolist() if "id" in usable.columns else list(range(len(usable)))
        return [
            {"id": int(ids[i]) if ids[i] is not None else None,
             "cluster": int(labels[i]),
             "label": cluster_labels[int(labels[i])]}
            for i in range(len(usable))
        ]

    def depreciation(self, brand: str, model: str) -> dict:
        subset = self.df[(self.df["brand"] == brand) & (self.df["model1"] == model)].copy()
        subset["_age"] = age_series(subset["vehicleage"])
        subset = subset.dropna(subset=["_age", "discountprice"])
        subset = subset[subset["discountprice"] > 0]
        n = len(subset)
        if n < 5:
            return {"error": "insufficient data", "n_samples": n}

        ages = subset["_age"].astype(float).values
        prices = subset["discountprice"].astype(float).values
        try:
            popt, _ = curve_fit(_exp_decay, ages, prices, p0=[prices.max(), 0.1], maxfev=5000)
        except (RuntimeError, ValueError):
            return {"error": "insufficient data", "n_samples": n}

        a, b = float(popt[0]), float(popt[1])
        observed = [
            {"age": float(ages[i]), "price": round(float(prices[i]), 2)}
            for i in range(n)
        ]
        fit_ages = np.linspace(ages.min(), ages.max(), num=min(50, max(10, n)))
        fitted = [
            {"age": round(float(age), 2), "price": round(float(_exp_decay(age, a, b)), 2)}
            for age in fit_ages
        ]
        return {
            "a": round(a, 4),
            "b": round(b, 4),
            "observed": observed,
            "fitted": fitted,
            "n_samples": n,
        }

    def anomalies(self, contamination: float = 0.05) -> list:
        data = self.df.copy()
        data["_age"] = age_series(data["vehicleage"])
        data = data.dropna(subset=["discountprice", "_age", "kilometer"])
        results = []
        for (brand, model), grp in data.groupby(["brand", "model1"]):
            if len(grp) < 10:
                continue
            features = grp[["discountprice", "_age", "kilometer"]].astype(float).values
            iso = IsolationForest(contamination=contamination, random_state=42)
            flags = iso.fit_predict(features)
            scores = iso.decision_function(features)
            median_price = float(grp["discountprice"].median())
            for idx_i, pos in enumerate(grp.index):
                if flags[idx_i] != -1:
                    continue
                row = grp.loc[pos]
                results.append({
                    "id": int(row["id"]) if "id" in grp.columns and pd.notna(row.get("id")) else None,
                    "brand": brand,
                    "model1": model,
                    "discountprice": round(float(row["discountprice"]), 2),
                    "group_median_price": round(median_price, 2),
                    "anomaly_score": round(float(scores[idx_i]), 4),
                })
        results.sort(key=lambda r: r["discountprice"] - r["group_median_price"])
        return results

    def _bucketed(self, granularity: str) -> pd.DataFrame:
        if granularity not in _GRANULARITY:
            raise ValueError(f"unsupported granularity: {granularity}")
        if "addtime" not in self.df.columns or "discountprice" not in self.df.columns:
            return pd.DataFrame(columns=["avg_price", "volume"])
        frame = self.df.dropna(subset=["addtime", "discountprice"]).copy()
        if frame.empty:
            return pd.DataFrame(columns=["avg_price", "volume"])
        frame = frame.set_index("addtime").sort_index()
        freq = _GRANULARITY[granularity]
        grouped = frame["discountprice"].astype(float).resample(freq).agg(["mean", "count"])
        grouped = grouped.rename(columns={"mean": "avg_price", "count": "volume"}).dropna(subset=["avg_price"])
        return grouped

    @staticmethod
    def _lag_features(prices):
        rows_X, rows_y = [], []
        for i in range(3, len(prices)):
            window = prices[max(0, i - 3):i]
            rows_X.append([
                prices[i - 1], prices[i - 2], prices[i - 3],
                float(np.mean(window)), float(np.std(window)),
            ])
            rows_y.append(prices[i])
        return np.array(rows_X), np.array(rows_y)

    @staticmethod
    def _lag_row(history):
        window = history[-3:]
        return np.array([[
            history[-1], history[-2], history[-3],
            float(np.mean(window)), float(np.std(window)),
        ]])

    @staticmethod
    def _tertile_tags(values: pd.Series, labels: tuple) -> dict:
        order = values.rank(method="min").astype(int) - 1
        n = len(values)
        out = {}
        for idx, rank in order.items():
            bucket = min(len(labels) - 1, int(rank * len(labels) / max(n, 1)))
            out[idx] = labels[bucket]
        return out
