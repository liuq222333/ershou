# coding:utf-8
__author__ = "ila"

import logging, os, json, configparser
import time
from collections import defaultdict
import numbers
import requests
from werkzeug.utils import redirect
import base64
import copy
from flask import request, jsonify, session
from sqlalchemy.sql import func, and_, or_, case
from sqlalchemy import cast, Integer, Float
from api.models.brush_model import *
from . import main_bp
from utils.codes import *
from utils.jwt_auth import Auth
from configs import configs
from utils.helper import *
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from utils.baidubce_api import BaiDuBce
from api.models.config_model import config
from flask import current_app as app
from utils.spark_func import spark_read_mysql
from utils.hdfs_func import upload_to_hdfs
from utils.mapreduce1 import MRMySQLAvg
import pandas as pd
import pymysql
from utils.configread import config_read
from sqlalchemy import create_engine
from utils.ml_price import PricePredictor, FEATURE_COLUMNS
from utils.deepseek_api import stream_analyze
from flask import Response, stream_with_context

pd.options.mode.chained_assignment = None
parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dbtype, host, port, user, passwd, dbName, charset, hasHadoop = config_read(os.path.join(parent_directory, "config.ini"))
mysql_config = {
    'host': host,
    'user': user,
    'password': passwd,
    'database': dbName,
    'port': port,
}
MODEL_DIR = os.path.join(parent_directory, "models")


def _usedcar_dataframe() -> pd.DataFrame:
    connection = pymysql.connect(**mysql_config)
    try:
        return pd.read_sql("SELECT brand,model1,vehicleage,kilometer,city,discountprice FROM usedcar", connection)
    finally:
        connection.close()


def _get_or_train_predictor() -> PricePredictor:
    predictor = PricePredictor(model_dir=MODEL_DIR)
    if predictor.is_trained:
        predictor.load()
    else:
        predictor.train(_usedcar_dataframe())
    return predictor


# 获取预测可视化图表接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/forecastimgs", methods=['GET', 'POST'])
def usedcarforecast_forecastimgs():
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, 'message': 'success', 'data': []}
        directory = os.path.join(parent_directory, "api", "templates", "upload", "usedcarforecast")
        if os.path.isdir(directory):
            all_items = os.listdir(directory)
            msg["data"] = [
                f'upload/usedcarforecast/{item}'
                for item in all_items
                if os.path.isfile(os.path.join(directory, item))
            ]
        return jsonify(msg)


@main_bp.route("/ershouche7de79q94/usedcarforecast/forecast", methods=['GET', 'POST'])
def usedcarforecast_forecast():
    if request.method not in ["POST", "GET"]:
        return jsonify({"code": normal_code, "msg": "success"})

    req_dict = dict(session.get("req_dict") or {})
    id_ = req_dict.pop("id", None)
    req_dict.pop("addtime", None)

    try:
        predictor = _get_or_train_predictor()
    except Exception as e:
        return jsonify({"code": other_code, "msg": f"training failed: {e}"})

    features = {col: req_dict.get(col) for col in FEATURE_COLUMNS}
    prediction = predictor.predict([features])[0]
    mid = prediction["mid"]

    connection_string = (
        f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}"
        f"@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"
    )
    engine = create_engine(connection_string)
    try:
        with engine.connect() as connection:
            if id_ is not None:
                connection.execute(
                    "UPDATE usedcarforecast SET discountprice = %(discountprice)s WHERE id = %(id)s",
                    {"id": id_, "discountprice": mid},
                )
            else:
                row = pd.DataFrame([{**features, "discountprice": mid}])
                row.to_sql("usedcarforecast", con=engine, if_exists="append", index=False)
    finally:
        engine.dispose()

    return jsonify({
        "code": normal_code,
        "msg": "success",
        "data": {
            "low": prediction["low"],
            "mid": prediction["mid"],
            "high": prediction["high"],
            "metrics": predictor.metrics(),
        },
    })


@main_bp.route("/ershouche7de79q94/usedcarforecast/retrain", methods=['GET', 'POST'])
def usedcarforecast_retrain():
    predictor = PricePredictor(model_dir=MODEL_DIR)
    try:
        metrics = predictor.train(_usedcar_dataframe())
    except Exception as e:
        return jsonify({"code": other_code, "msg": f"training failed: {e}"})
    return jsonify({"code": normal_code, "msg": "success", "data": metrics})


# 分类接口（后端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/page", methods=['GET'])
def ershouche7de79q94_usedcarforecast_page():
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = session.get("req_dict")
        has_userid = 'userid' in req_dict
        userinfo = session.get("params")
        tablename = session.get("tablename")

        clause_args = []
        or_clauses = or_(*clause_args)
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = usedcarforecast.page(usedcarforecast, usedcarforecast, req_dict, or_clauses)
        return jsonify(msg)


# 排序接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/autoSort", methods=['GET'])
def ershouche7de79q94_usedcarforecast_autosort():
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = session.get("req_dict")
        req_dict['sort'] = 'clicktime'
        req_dict['order'] = 'desc'

        try:
            __browseClick__ = usedcarforecast.__browseClick__
        except:
            __browseClick__ = None
        if __browseClick__ == '是':
            req_dict['sort'] = 'clicknum'
        elif __browseClick__ == '时长':
            req_dict['sort'] = 'browseduration'
        else:
            req_dict['sort'] = 'clicktime'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = usedcarforecast.page(usedcarforecast, usedcarforecast, req_dict)

        return jsonify(msg)


# 查询单条数据
@main_bp.route("/ershouche7de79q94/usedcarforecast/query", methods=['GET'])
def ershouche7de79q94_usedcarforecast_query():
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        query = db.session.query(usedcarforecast)
        for key, value in req_dict.items():
            query = query.filter(getattr(usedcarforecast, key) == value)
        query_result = query.first()
        query_result.__dict__.pop('_sa_instance_state', None)
        msg['data'] = query_result.__dict__
        return jsonify(msg)


# 分页接口（前端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/list", methods=['GET'])
def ershouche7de79q94_usedcarforecast_list():
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']

        userinfo = session.get("params")

        try:
            __foreEndListAuth__ = usedcarforecast.__foreEndListAuth__
        except:
            __foreEndListAuth__ = None
        if __foreEndListAuth__ and __foreEndListAuth__ != "否":
            tablename = session.get("tablename")
            if tablename != "users" and session.get("params") is not None:
                req_dict['userid'] = session.get("params").get("id")
        tablename = session.get("tablename")
        if 'luntan' in 'usedcarforecast':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        if 'discuss' in 'usedcarforecast':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = usedcarforecast.page(usedcarforecast, usedcarforecast, req_dict)
        return jsonify(msg)


# 保存接口（后端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/save", methods=['POST'])
def ershouche7de79q94_usedcarforecast_save():
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        for key in req_dict:
            if req_dict[key] == '':
                req_dict[key] = None

        error = usedcarforecast.createbyreq(usedcarforecast, usedcarforecast, req_dict)
        if error is not None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return jsonify(msg)


# 添加接口（前端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/add", methods=['POST'])
def ershouche7de79q94_usedcarforecast_add():
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        try:
            __foreEndListAuth__ = usedcarforecast.__foreEndListAuth__
        except:
            __foreEndListAuth__ = None
        if __foreEndListAuth__ and __foreEndListAuth__ != "否":
            tablename = session.get("tablename")
            if tablename != "users":
                req_dict['userid'] = session.get("params").get("id")

        error = usedcarforecast.createbyreq(usedcarforecast, usedcarforecast, req_dict)
        if error is not None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
            return jsonify(msg)
        else:
            msg['data'] = error
        return jsonify(msg)


# 踩、赞接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/thumbsup/<id_>", methods=['GET'])
def ershouche7de79q94_usedcarforecast_thumbsup(id_):
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        id_ = int(id_)
        type_ = int(req_dict.get("type", 0))
        rets = usedcarforecast.getbyid(usedcarforecast, usedcarforecast, id_)
        update_dict = {"id": id_}
        if type_ == 1:
            update_dict["thumbsupnum"] = int(rets[0].get('thumbsupnum')) + 1
        elif type_ == 2:
            update_dict["crazilynum"] = int(rets[0].get('crazilynum')) + 1
        error = usedcarforecast.updatebyparams(usedcarforecast, usedcarforecast, update_dict)
        if error is not None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)


# 获取详情信息（后端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/info/<id_>", methods=['GET'])
def ershouche7de79q94_usedcarforecast_info(id_):
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        data = usedcarforecast.getbyid(usedcarforecast, usedcarforecast, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]
        try:
            __browseClick__ = usedcarforecast.__browseClick__
        except:
            __browseClick__ = None

        if __browseClick__ and "clicknum" in usedcarforecast.__table__.columns:
            click_dict = {"id": int(id_), "clicknum": str(int(data[0].get("clicknum") or 0) + 1)}
            ret = usedcarforecast.updatebyparams(usedcarforecast, usedcarforecast, click_dict)
            if ret is not None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)


# 获取详情信息（前端）
@main_bp.route("/ershouche7de79q94/usedcarforecast/detail/<id_>", methods=['GET'])
def ershouche7de79q94_usedcarforecast_detail(id_):
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        data = usedcarforecast.getbyid(usedcarforecast, usedcarforecast, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]

        try:
            __browseClick__ = usedcarforecast.__browseClick__
        except:
            __browseClick__ = None

        if __browseClick__ and "clicknum" in usedcarforecast.__table__.columns:
            click_dict = {"id": int(id_), "clicknum": str(int(data[0].get("clicknum") or 0) + 1)}
            ret = usedcarforecast.updatebyparams(usedcarforecast, usedcarforecast, click_dict)
            if ret is not None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)


# 更新接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/update", methods=['POST'])
def ershouche7de79q94_usedcarforecast_update():
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        if req_dict.get("mima") and "mima" not in usedcarforecast.__table__.columns:
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in usedcarforecast.__table__.columns:
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass

        error = usedcarforecast.updatebyparams(usedcarforecast, usedcarforecast, req_dict)
        if error is not None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return jsonify(msg)


# 删除接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/delete", methods=['POST'])
def ershouche7de79q94_usedcarforecast_delete():
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        error = usedcarforecast.delete(usedcarforecast, req_dict)
        if error is not None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)


# 投票接口
@main_bp.route("/ershouche7de79q94/usedcarforecast/vote/<int:id_>", methods=['POST'])
def ershouche7de79q94_usedcarforecast_vote(id_):
    if request.method == 'POST':
        msg = {"code": normal_code, "msg": "success"}
        data = usedcarforecast.getbyid(usedcarforecast, usedcarforecast, int(id_))
        for i in data:
            votenum = i.get('votenum')
            if votenum is not None:
                params = {"id": int(id_), "votenum": votenum + 1}
                error = usedcarforecast.updatebyparams(usedcarforecast, usedcarforecast, params)
                if error is not None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return jsonify(msg)


# 获取所有记录列表
@main_bp.route("/ershouche7de79q94/usedcarforecast/lists", methods=['GET'])
def ershouche7de79q94_usedcarforecast_lists():
    if request.method == 'GET':
        msg = {"code": normal_code, "msg": "success", "data": []}
        req_dict = session.get("req_dict")
        list, _, _, _, _ = usedcarforecast.page(usedcarforecast, usedcarforecast, req_dict)
        msg['data'] = list
        return jsonify(msg)


def _market_stats(brand: str, city: str) -> dict:
    connection = pymysql.connect(**mysql_config)
    try:
        df = pd.read_sql("SELECT brand, city, discountprice FROM usedcar", connection)
    finally:
        connection.close()

    df["discountprice"] = pd.to_numeric(df["discountprice"], errors="coerce")
    df = df.dropna(subset=["discountprice"])

    brand_df = df[df["brand"] == brand]
    city_df = df[df["city"] == city]

    return {
        "brand_count": int(len(brand_df)),
        "brand_avg_price": round(float(brand_df["discountprice"].mean()), 2) if len(brand_df) else "—",
        "city_count": int(len(city_df)),
        "city_avg_price": round(float(city_df["discountprice"].mean()), 2) if len(city_df) else "—",
        "total_avg_price": round(float(df["discountprice"].mean()), 2) if len(df) else "—",
    }


@main_bp.route("/ershouche7de79q94/usedcarforecast/ai_analyze", methods=["GET", "POST"])
def usedcarforecast_ai_analyze():
    req_dict = dict(session.get("req_dict") or {})

    try:
        predictor = _get_or_train_predictor()
    except Exception as e:
        return jsonify({"code": other_code, "msg": f"model error: {e}"})

    features = {col: req_dict.get(col) for col in FEATURE_COLUMNS}
    prediction = predictor.predict([features])[0]

    car_info = {
        "brand": req_dict.get("brand", ""),
        "model1": req_dict.get("model1", ""),
        "vehicleage": req_dict.get("vehicleage", ""),
        "kilometer": req_dict.get("kilometer", ""),
        "city": req_dict.get("city", ""),
    }

    stats = _market_stats(car_info["brand"], car_info["city"])

    def generate():
        try:
            for chunk in stream_analyze(car_info, prediction, stats):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
