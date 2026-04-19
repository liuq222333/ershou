# coding:utf-8
import math

import numpy as np
import pandas as pd
import pytest

from utils.ml_trend import TrendAnalyzer


BRANDS = ["A", "B", "C"]
MODELS = ["X", "Y"]
CITIES = ["北京", "上海", "深圳"]


def _make_df(n_rows=120, start="2023-01-01", end="2024-12-20"):
    np.random.seed(42)
    dates = pd.to_datetime(
        np.random.choice(pd.date_range(start=start, end=end, freq="D"), size=n_rows)
    )
    brands = np.random.choice(BRANDS, size=n_rows)
    models = np.random.choice(MODELS, size=n_rows)
    cities = np.random.choice(CITIES, size=n_rows)
    years = np.random.randint(2015, 2025, size=n_rows)
    vehicleage = [f"{y}年" for y in years]
    km = np.random.uniform(0.5, 15.0, size=n_rows)
    age = 2025 - years
    price = 22.0 - 1.1 * age - 0.35 * km + np.random.normal(0, 0.7, size=n_rows)
    price = np.clip(price, 1.0, None)
    return pd.DataFrame({
        "id": np.arange(1, n_rows + 1),
        "addtime": dates,
        "brand": brands,
        "model1": models,
        "city": cities,
        "vehicleage": vehicleage,
        "kilometer": km,
        "discountprice": price,
    })


@pytest.fixture(scope="module")
def trend_df():
    return _make_df()


@pytest.fixture()
def analyzer(trend_df):
    return TrendAnalyzer(trend_df)


def test_timeseries_month_sorted_and_shape(analyzer):
    out = analyzer.timeseries("month")
    assert len(out) > 0
    periods = [entry["period"] for entry in out]
    assert periods == sorted(periods)
    expected_keys = {"period", "avg_price", "volume", "rolling_avg_price"}
    for entry in out:
        assert set(entry.keys()) == expected_keys
        assert math.isfinite(entry["avg_price"])
        assert entry["volume"] >= 1
        assert math.isfinite(entry["rolling_avg_price"])


@pytest.mark.parametrize("granularity", ["day", "month"])
def test_timeseries_any_granularity_non_empty(analyzer, granularity):
    assert len(analyzer.timeseries(granularity)) > 0


def test_timeseries_year_granularity(analyzer):
    assert len(analyzer.timeseries("year")) > 0


def test_forecast_monthly_horizon_six(analyzer):
    out = analyzer.forecast(6, "month")
    assert len(out) == 6
    for entry in out:
        assert entry["is_forecast"] is True
        assert not math.isnan(entry["forecast_price"])


def test_forecast_fallback_when_few_periods():
    tiny_df = _make_df(n_rows=15, start="2024-01-01", end="2024-04-30")
    small = TrendAnalyzer(tiny_df)
    out = small.forecast(4, "month")
    assert len(out) == 4
    assert all(entry.get("fallback") is True for entry in out)
    assert all(entry["is_forecast"] is True for entry in out)


def test_decompose_structure_and_identity(analyzer):
    result = analyzer.decompose("month")
    keys = ["period", "observed", "trend", "seasonal", "residual"]
    lengths = {k: len(result[k]) for k in keys}
    assert len(set(lengths.values())) == 1
    n = lengths["period"]
    assert n > 0
    obs = np.array(result["observed"])
    trend = np.array(result["trend"])
    seasonal = np.array(result["seasonal"])
    residual = np.array(result["residual"])
    # residual definition: observed - trend - seasonal; values are rounded
    # to 2dp independently, so allow 0.05 absolute tolerance.
    assert np.allclose(obs, trend + seasonal + residual, atol=0.05, equal_nan=False)


def test_cluster_labels_in_range(analyzer, trend_df):
    out = analyzer.cluster(k=3)
    assert len(out) > 0
    for entry in out:
        assert entry["cluster"] in {0, 1, 2}
        assert isinstance(entry["label"], str) and entry["label"]
    # every row with complete features should be clustered
    assert len(out) == len(trend_df.dropna(subset=["discountprice", "kilometer"]))


def test_depreciation_valid_brand_model(trend_df):
    analyzer = TrendAnalyzer(trend_df)
    out = analyzer.depreciation("A", "X")
    assert "error" not in out
    assert math.isfinite(out["a"])
    assert math.isfinite(out["b"])
    assert len(out["observed"]) > 0
    assert len(out["fitted"]) > 0


def test_depreciation_missing_brand_returns_error(analyzer):
    out = analyzer.depreciation("ZZZ_MISSING", "NOPE")
    assert "error" in out
    assert out["n_samples"] == 0


def test_anomalies_flags_injected_outliers():
    np.random.seed(42)
    # build 18 rows all in brand A / model X / year 2020 so group size >= 10
    n = 18
    df = pd.DataFrame({
        "id": np.arange(1, n + 1),
        "addtime": pd.date_range("2024-01-01", periods=n, freq="D"),
        "brand": ["A"] * n,
        "model1": ["X"] * n,
        "city": ["北京"] * n,
        "vehicleage": ["2020年"] * n,
        "kilometer": np.random.uniform(4.0, 8.0, size=n),
        "discountprice": np.random.normal(15.0, 0.4, size=n),
    })
    df.loc[df.index[0], "discountprice"] = 0.5
    df.loc[df.index[1], "discountprice"] = 0.8
    outlier_ids = {int(df.loc[df.index[0], "id"]), int(df.loc[df.index[1], "id"])}

    analyzer = TrendAnalyzer(df)
    result = analyzer.anomalies(contamination=0.15)
    flagged_ids = {entry["id"] for entry in result}
    assert outlier_ids.issubset(flagged_ids)


def test_timeseries_unknown_granularity_raises(analyzer):
    with pytest.raises(ValueError):
        analyzer.timeseries("hour")
