# coding:utf-8
__author__ = "ila"

import os

import pandas as pd
import pymysql
from flask import jsonify, request, session

from . import main_bp
from utils.codes import normal_code, other_code
from utils.configread import config_read
from utils.ml_trend import TrendAnalyzer

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dbtype, host, port, user, passwd, dbName, charset, hasHadoop = config_read(
    os.path.join(parent_directory, "config.ini")
)
mysql_config = {
    "host": host,
    "user": user,
    "password": passwd,
    "database": dbName,
    "port": port,
}

USEDCAR_QUERY = (
    "SELECT id, addtime, brand, model1, discountprice, vehicleage, kilometer, city FROM usedcar"
)


def _load_df() -> pd.DataFrame:
    connection = pymysql.connect(**mysql_config)
    try:
        return pd.read_sql(USEDCAR_QUERY, connection)
    finally:
        connection.close()


def _ok(data):
    return jsonify({"code": normal_code, "msg": "success", "data": data})


def _fail(msg: str):
    return jsonify({"code": other_code, "msg": msg})


@main_bp.route("/ershouche7de79q94/trend/timeseries/<granularity>", methods=["GET"])
def trend_timeseries(granularity):
    if granularity not in ("day", "month", "year"):
        return _fail("granularity must be one of day|month|year")
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.timeseries(granularity)
    if not data:
        return _fail("insufficient data")
    return _ok(data)


@main_bp.route("/ershouche7de79q94/trend/forecast/<int:horizon>", methods=["GET"])
def trend_forecast(horizon):
    req_dict = session.get("req_dict") or {}
    granularity = req_dict.get("granularity", "month")
    if granularity not in ("day", "month", "year"):
        return _fail("granularity must be one of day|month|year")
    if horizon <= 0:
        return _fail("horizon must be positive")
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.forecast(horizon, granularity)
    if not data:
        return _fail("insufficient data")
    return _ok(data)


@main_bp.route("/ershouche7de79q94/trend/decompose", methods=["GET"])
def trend_decompose():
    req_dict = session.get("req_dict") or {}
    granularity = req_dict.get("granularity", "month")
    if granularity not in ("day", "month", "year"):
        return _fail("granularity must be one of day|month|year")
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.decompose(granularity)
    if not data.get("period"):
        return _fail("insufficient data")
    return _ok(data)


@main_bp.route("/ershouche7de79q94/trend/cluster", methods=["GET"])
def trend_cluster():
    req_dict = session.get("req_dict") or {}
    k = int(req_dict.get("k", 4))
    if k < 2:
        return _fail("k must be >= 2")
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.cluster(k)
    if not data:
        return _fail("insufficient data")
    return _ok(data)


@main_bp.route("/ershouche7de79q94/trend/depreciation/<brand>/<model>", methods=["GET"])
def trend_depreciation(brand, model):
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.depreciation(brand, model)
    if "error" in data:
        return _fail(data["error"])
    return _ok(data)


@main_bp.route("/ershouche7de79q94/trend/anomaly", methods=["GET"])
def trend_anomaly():
    req_dict = session.get("req_dict") or {}
    contamination = float(req_dict.get("contamination", 0.05))
    if not 0 < contamination < 0.5:
        return _fail("contamination must be in (0, 0.5)")
    analyzer = TrendAnalyzer(_load_df())
    data = analyzer.anomalies(contamination)
    return _ok(data)
