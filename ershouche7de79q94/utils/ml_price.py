# coding:utf-8
import os
from datetime import datetime
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from utils._ml_common import vehicleage_to_age

FEATURE_COLUMNS = ["brand", "model1", "vehicleage", "kilometer", "city"]
CATEGORICAL = ["brand", "model1", "city"]
TARGET = "discountprice"
PICKLE_NAME = "price_pipeline.pkl"


def _age_transform(X):
    arr = np.asarray(X).ravel()
    return vehicleage_to_age(arr).reshape(-1, 1)


def _build_preprocessor() -> ColumnTransformer:
    age_pipe = Pipeline(steps=[
        ("parse", FunctionTransformer(_age_transform, validate=False)),
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    km_pipe = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    cat_pipe = Pipeline(steps=[
        ("impute", SimpleImputer(strategy="constant", fill_value="")),
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer(
        transformers=[
            ("age", age_pipe, ["vehicleage"]),
            ("km", km_pipe, ["kilometer"]),
            ("cat", cat_pipe, CATEGORICAL),
        ],
        sparse_threshold=0,
    )


def _make_regressor(quantile: float) -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        loss="quantile",
        quantile=quantile,
        max_iter=200,
        learning_rate=0.08,
        max_depth=None,
        random_state=42,
    )


class PricePredictor:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self._pipeline_q10: Optional[Pipeline] = None
        self._pipeline_q50: Optional[Pipeline] = None
        self._pipeline_q90: Optional[Pipeline] = None
        self._metrics: Optional[dict] = None

    @property
    def pickle_path(self) -> str:
        return os.path.join(self.model_dir, PICKLE_NAME)

    @property
    def is_trained(self) -> bool:
        return os.path.isfile(self.pickle_path)

    def metrics(self) -> Optional[dict]:
        return self._metrics

    def train(self, df: pd.DataFrame) -> dict:
        data = df[FEATURE_COLUMNS + [TARGET]].dropna(subset=[TARGET]).copy()
        X = data[FEATURE_COLUMNS]
        y = data[TARGET].astype(float).values

        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self._pipeline_q10 = Pipeline([("pre", _build_preprocessor()), ("reg", _make_regressor(0.1))])
        self._pipeline_q50 = Pipeline([("pre", _build_preprocessor()), ("reg", _make_regressor(0.5))])
        self._pipeline_q90 = Pipeline([("pre", _build_preprocessor()), ("reg", _make_regressor(0.9))])

        self._pipeline_q10.fit(x_train, y_train)
        self._pipeline_q50.fit(x_train, y_train)
        self._pipeline_q90.fit(x_train, y_train)

        y_pred = self._pipeline_q50.predict(x_test)
        self._metrics = {
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "r2": float(r2_score(y_test, y_pred)),
            "n_train": int(len(x_train)),
            "n_test": int(len(x_test)),
            "trained_at": datetime.now().isoformat(timespec="seconds"),
        }
        self._persist()
        return self._metrics

    def load(self) -> None:
        if not self.is_trained:
            raise FileNotFoundError(f"model pickle not found: {self.pickle_path}")
        bundle = joblib.load(self.pickle_path)
        self._pipeline_q10 = bundle["q10"]
        self._pipeline_q50 = bundle["q50"]
        self._pipeline_q90 = bundle["q90"]
        self._metrics = bundle.get("metrics")

    def predict(self, records: list) -> list:
        if self._pipeline_q50 is None:
            self.load()
        frame = pd.DataFrame([self._normalize_record(r) for r in records], columns=FEATURE_COLUMNS)
        low = self._pipeline_q10.predict(frame)
        mid = self._pipeline_q50.predict(frame)
        high = self._pipeline_q90.predict(frame)
        low, high = np.minimum(low, high), np.maximum(low, high)
        mid = np.clip(mid, low, high)
        return [
            {"low": round(float(low[i]), 2), "mid": round(float(mid[i]), 2), "high": round(float(high[i]), 2)}
            for i in range(len(frame))
        ]

    def _persist(self) -> None:
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(
            {
                "q10": self._pipeline_q10,
                "q50": self._pipeline_q50,
                "q90": self._pipeline_q90,
                "metrics": self._metrics,
            },
            self.pickle_path,
        )

    @staticmethod
    def _normalize_record(record: dict) -> dict:
        out = {}
        for col in FEATURE_COLUMNS:
            val = record.get(col, None)
            if col in CATEGORICAL:
                out[col] = "" if val is None else str(val)
            else:
                out[col] = val
        return out
