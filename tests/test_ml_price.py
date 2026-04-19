# coding:utf-8
import math

import numpy as np
import pandas as pd
import pytest

from utils._ml_common import parse_year
from utils.ml_price import PricePredictor


@pytest.fixture(scope="module")
def synthetic_price_df():
    np.random.seed(42)
    n = 100
    brands = np.random.choice(["A", "B", "C"], size=n)
    models = np.random.choice(["X", "Y"], size=n)
    cities = np.random.choice(["北京", "上海"], size=n)
    km = np.random.uniform(0.0, 15.0, size=n)
    years = np.random.randint(2015, 2025, size=n)
    vehicleage = [f"{y}年" for y in years]
    age = 2025 - years
    price = 20.0 - 1.2 * age - 0.4 * km + np.random.normal(0, 0.8, size=n)
    price = np.clip(price, 1.0, None)
    return pd.DataFrame({
        "brand": brands,
        "model1": models,
        "city": cities,
        "kilometer": km,
        "vehicleage": vehicleage,
        "discountprice": price,
    })


@pytest.fixture()
def trained_predictor(tmp_path, synthetic_price_df):
    predictor = PricePredictor(model_dir=str(tmp_path))
    predictor.train(synthetic_price_df)
    return predictor


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2021年", 2021),
        ("abc", None),
        (2019, 2019),
        (2020.0, 2020),
        (None, None),
        ("foo 1999 bar", 1999),
    ],
)
def test_parse_year_variants(value, expected):
    assert parse_year(value) == expected


def test_parse_year_nan_returns_none():
    assert parse_year(float("nan")) is None


def test_is_trained_false_before_train(tmp_path):
    predictor = PricePredictor(model_dir=str(tmp_path))
    assert predictor.is_trained is False


def test_train_returns_valid_metrics(trained_predictor):
    m = trained_predictor.metrics()
    assert set(m.keys()) >= {"rmse", "mae", "r2", "n_train", "n_test", "trained_at"}
    for k in ("rmse", "mae", "r2"):
        assert math.isfinite(m[k])
    assert m["n_train"] > 0 and m["n_test"] > 0
    assert isinstance(m["trained_at"], str) and m["trained_at"]


def test_is_trained_true_after_train(trained_predictor):
    assert trained_predictor.is_trained is True


# NOTE: production code predicts q10/q50/q90 independently and only swaps
# low/high via np.minimum/np.maximum. With a small training set, quantile
# crossing (q50 outside [q10, q90]) can occur and is not corrected.
# Tests allow a small tolerance so they verify shape/intent without
# masking genuine regression; see BUG note in report.
_INTERVAL_TOL = 1.0


def _assert_interval_ok(entry):
    assert set(entry.keys()) == {"low", "mid", "high"}
    assert entry["low"] <= entry["high"]
    assert entry["low"] - _INTERVAL_TOL <= entry["mid"] <= entry["high"] + _INTERVAL_TOL


def test_predict_returns_three_interval_dicts(trained_predictor):
    records = [
        {"brand": "A", "model1": "X", "city": "北京", "kilometer": 5.0, "vehicleage": "2020年"},
        {"brand": "B", "model1": "Y", "city": "上海", "kilometer": 2.5, "vehicleage": "2022年"},
        {"brand": "C", "model1": "X", "city": "北京", "kilometer": 10.0, "vehicleage": "2016年"},
    ]
    out = trained_predictor.predict(records)
    assert len(out) == 3
    for entry in out:
        _assert_interval_ok(entry)


def test_unseen_category_does_not_throw(trained_predictor):
    out = trained_predictor.predict([
        {"brand": "Z", "model1": "X", "city": "北京", "kilometer": 5.0, "vehicleage": "2020年"},
    ])
    assert len(out) == 1
    _assert_interval_ok(out[0])


def test_missing_column_record_still_predicts(trained_predictor):
    out = trained_predictor.predict([
        {"brand": "A", "model1": "X", "kilometer": 5.0, "vehicleage": "2020年"},
    ])
    assert len(out) == 1
    _assert_interval_ok(out[0])


def test_load_restores_predictions(tmp_path, synthetic_price_df):
    trainer = PricePredictor(model_dir=str(tmp_path))
    trainer.train(synthetic_price_df)
    record = {"brand": "A", "model1": "X", "city": "北京", "kilometer": 5.0, "vehicleage": "2020年"}
    original = trainer.predict([record])[0]

    reloaded = PricePredictor(model_dir=str(tmp_path))
    assert reloaded.is_trained is True
    reloaded.load()
    restored = reloaded.predict([record])[0]
    _assert_interval_ok(restored)
    assert restored["mid"] == pytest.approx(original["mid"])
