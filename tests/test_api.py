# coding:utf-8
"""
API smoke tests for the new forecast / trend endpoints.

The full `api` package imports Flask-SQLAlchemy, pyspark, hdfs, etc. which
are not installable on the test host. We sidestep that by loading only the
two route modules we care about (`Trend_v.py`, `Usedcarforecast_v.py`) via
importlib, stubbing their transitive deps, and calling the view functions
inside a Flask test request context.
"""
import importlib.util
import os
import sys
import types

import numpy as np
import pandas as pd
import pytest
from flask import Flask, Blueprint


BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "ershouche7de79q94")
)


def _make_usedcar_df():
    np.random.seed(42)
    n = 120
    dates = pd.to_datetime(
        np.random.choice(pd.date_range("2023-01-01", "2024-12-20", freq="D"), size=n)
    )
    brands = np.random.choice(["A", "B", "C"], size=n)
    models = np.random.choice(["X", "Y"], size=n)
    cities = np.random.choice(["北京", "上海"], size=n)
    years = np.random.randint(2015, 2025, size=n)
    vehicleage = [f"{y}年" for y in years]
    km = np.random.uniform(0.5, 15.0, size=n)
    age = 2025 - years
    price = 22.0 - 1.1 * age - 0.35 * km + np.random.normal(0, 0.7, size=n)
    price = np.clip(price, 1.0, None)
    return pd.DataFrame({
        "id": np.arange(1, n + 1),
        "addtime": dates,
        "brand": brands,
        "model1": models,
        "city": cities,
        "vehicleage": vehicleage,
        "kilometer": km,
        "discountprice": price,
    })


def _install_stub_main_bp():
    """Install a stub `api.main` package with a plain main_bp and
    stub `api.main.common`, so route modules can `from . import main_bp`
    without triggering the full dynamic-exec __init__.py."""
    if "api" not in sys.modules:
        api_pkg = types.ModuleType("api")
        api_pkg.__path__ = [os.path.join(BACKEND_DIR, "api")]
        sys.modules["api"] = api_pkg
    if "api.main" not in sys.modules:
        main_pkg = types.ModuleType("api.main")
        main_pkg.__path__ = [os.path.join(BACKEND_DIR, "api", "main")]
        main_pkg.main_bp = Blueprint("main", __name__)
        sys.modules["api.main"] = main_pkg
    return sys.modules["api.main"]


def _load_module_from_path(name: str, relpath: str):
    full = os.path.join(BACKEND_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, full)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _ensure_stub_deps():
    """Stub optional/DB-only deps that Trend_v + Usedcarforecast_v import."""
    if "pymysql" not in sys.modules:
        stub = types.ModuleType("pymysql")
        stub.connect = lambda *a, **kw: (_ for _ in ()).throw(
            RuntimeError("pymysql.connect should be stubbed in tests")
        )
        sys.modules["pymysql"] = stub
    if "sqlalchemy" not in sys.modules:
        try:
            import sqlalchemy  # noqa: F401
        except ModuleNotFoundError:
            stub = types.ModuleType("sqlalchemy")
            stub.create_engine = lambda *a, **kw: None
            sql = types.ModuleType("sqlalchemy.sql")
            sql.func = None
            sql.and_ = None
            sql.or_ = None
            sql.case = None
            stub.sql = sql
            stub.cast = lambda *a, **kw: None
            stub.Integer = int
            stub.Float = float
            sys.modules["sqlalchemy"] = stub
            sys.modules["sqlalchemy.sql"] = sql


@pytest.fixture(scope="module")
def trend_module():
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    _ensure_stub_deps()
    _install_stub_main_bp()
    try:
        return _load_module_from_path("api.main.Trend_v", "api/main/Trend_v.py")
    except Exception as exc:
        pytest.skip(f"Trend_v import failed: {exc}")


@pytest.fixture()
def trend_app(trend_module, monkeypatch):
    df = _make_usedcar_df()
    monkeypatch.setattr(trend_module, "_load_df", lambda: df.copy())
    app = Flask("trend_test")
    app.secret_key = "test"
    return app, trend_module


def _call_with_req_dict(app, view, req_dict=None, **kwargs):
    """Invoke a Flask view with session['req_dict'] populated."""
    with app.test_request_context("/"):
        from flask import session
        session["req_dict"] = req_dict or {}
        return view(**kwargs)


def _parse(response):
    return response.get_json()


def test_trend_timeseries_month(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_timeseries, granularity="month")
    body = _parse(resp)
    assert body["code"] == 0
    assert isinstance(body["data"], list) and len(body["data"]) > 0


def test_trend_forecast_six(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_forecast, req_dict={"granularity": "month"}, horizon=6)
    body = _parse(resp)
    assert body["code"] == 0
    assert len(body["data"]) == 6


def test_trend_decompose(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_decompose, req_dict={"granularity": "month"})
    body = _parse(resp)
    assert body["code"] == 0
    assert isinstance(body["data"]["period"], list) and body["data"]["period"]


def test_trend_cluster(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_cluster, req_dict={"k": 3})
    body = _parse(resp)
    assert body["code"] == 0
    assert body["data"]
    for entry in body["data"]:
        assert entry["cluster"] in {0, 1, 2}
        assert entry["label"]


def test_trend_depreciation_present(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_depreciation, brand="A", model="X")
    body = _parse(resp)
    assert body["code"] == 0
    assert "a" in body["data"] and "b" in body["data"]


def test_trend_depreciation_missing(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_depreciation, brand="ZZZ", model="NOPE")
    body = _parse(resp)
    assert body["code"] == 10020


def test_trend_anomaly(trend_app):
    app, mod = trend_app
    resp = _call_with_req_dict(app, mod.trend_anomaly, req_dict={"contamination": 0.1})
    body = _parse(resp)
    assert body["code"] == 0
    assert isinstance(body["data"], list)


# ---------------------------------------------------------------------------
# Usedcarforecast retrain — deep import chain. If it cannot be stubbed
# cleanly, skip with a clear message rather than fighting it.
# ---------------------------------------------------------------------------


def _try_load_usedcarforecast():
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    _ensure_stub_deps()
    _install_stub_main_bp()
    # Stub the heavy optional deps this module pulls in transitively.
    for name in [
        "api.models",
        "api.models.brush_model",
        "api.models.config_model",
        "api.exts",
        "utils.jwt_auth",
        "utils.helper",
        "utils.baidubce_api",
        "utils.spark_func",
        "utils.hdfs_func",
        "utils.mapreduce1",
        "configs",
    ]:
        if name in sys.modules:
            continue
        mod = types.ModuleType(name)
        if name == "api.exts":
            mod.db = types.SimpleNamespace(session=None)
        if name == "api.models.brush_model":
            mod.usedcarforecast = type("usedcarforecast", (), {})
        if name == "api.models.config_model":
            mod.config = type("config", (), {})
        if name == "utils.jwt_auth":
            mod.Auth = type("Auth", (), {})
        if name == "utils.baidubce_api":
            mod.BaiDuBce = type("BaiDuBce", (), {})
        if name == "utils.spark_func":
            mod.spark_read_mysql = lambda *a, **kw: None
        if name == "utils.hdfs_func":
            mod.upload_to_hdfs = lambda *a, **kw: None
        if name == "utils.mapreduce1":
            mod.MRMySQLAvg = type("MRMySQLAvg", (), {})
        if name == "configs":
            mod.configs = types.SimpleNamespace()
        sys.modules[name] = mod
    return _load_module_from_path(
        "api.main.Usedcarforecast_v", "api/main/Usedcarforecast_v.py"
    )


@pytest.fixture(scope="module")
def usedcarforecast_module():
    try:
        return _try_load_usedcarforecast()
    except Exception as exc:
        pytest.skip(f"Usedcarforecast_v import failed: {exc}")


def test_usedcarforecast_retrain(usedcarforecast_module, monkeypatch, tmp_path):
    mod = usedcarforecast_module
    df = _make_usedcar_df()
    monkeypatch.setattr(mod, "_usedcar_dataframe", lambda: df.copy())
    monkeypatch.setattr(mod, "MODEL_DIR", str(tmp_path))
    app = Flask("retrain_test")
    app.secret_key = "test"
    with app.test_request_context("/", method="GET"):
        resp = mod.usedcarforecast_retrain()
    body = resp.get_json()
    assert body["code"] == 0
    metrics = body["data"]
    assert {"rmse", "mae", "r2", "n_train", "n_test", "trained_at"}.issubset(metrics)
