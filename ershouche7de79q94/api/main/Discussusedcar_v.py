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
from flask import request, jsonify,session
from sqlalchemy.sql import func,and_,or_,case
from sqlalchemy import cast, Integer,Float
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
# 分类接口（后端）
@main_bp.route("/ershouche7de79q94/discussusedcar/page", methods=['GET'])
def ershouche7de79q94_discussusedcar_page():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        has_userid = 'userid' in req_dict
        userinfo = session.get("params")
        tablename=session.get("tablename")

        clause_args = []
        or_clauses = or_(*clause_args)
        #查询列表数据
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = discussusedcar.page(discussusedcar, discussusedcar, req_dict, or_clauses)
        return jsonify(msg)


# 排序接口
@main_bp.route("/ershouche7de79q94/discussusedcar/autoSort", methods=['GET'])
def ershouche7de79q94_discussusedcar_autosort():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        req_dict['sort']='clicktime'
        req_dict['order']='desc'

        try:#获取需要排序的内容
            __browseClick__= discussusedcar.__browseClick__
        except:
            __browseClick__=None
        #根据排序字段进行排序
        if __browseClick__ =='是':
            req_dict['sort']='clicknum'
        elif __browseClick__ =='时长':
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        #获取排序内容
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = discussusedcar.page(discussusedcar, discussusedcar, req_dict)

        return jsonify(msg)

#查询单条数据
@main_bp.route("/ershouche7de79q94/discussusedcar/query", methods=['GET'])
def ershouche7de79q94_discussusedcar_query():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{}}
        #获取传递的参数，根据参数获取单条结果
        req_dict = session.get("req_dict")
        query = db.session.query(discussusedcar)
        for key, value in req_dict.items():
            query = query.filter(getattr(discussusedcar, key) == value)
        query_result = query.first()
        query_result.__dict__.pop('_sa_instance_state', None)
        msg['data'] = query_result.__dict__
        return jsonify(msg)

# 分页接口（前端）
@main_bp.route("/ershouche7de79q94/discussusedcar/list", methods=['GET'])
def ershouche7de79q94_discussusedcar_list():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']

        userinfo = session.get("params")

        try:#判断是否有列表权限
            __foreEndListAuth__=discussusedcar.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限判断就去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None:
                req_dict['userid']=session.get("params").get("id")
        tablename=session.get("tablename")
        if 'luntan' in 'discussusedcar':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        if 'discuss' in 'discussusedcar':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        #根据封装的req_dict字典去筛选获取列表数据
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = discussusedcar.page(discussusedcar, discussusedcar, req_dict)
        return jsonify(msg)

# 保存接口（后端）
@main_bp.route("/ershouche7de79q94/discussusedcar/save", methods=['POST'])
def ershouche7de79q94_discussusedcar_save():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        for key in req_dict:#将空值转为None
            if req_dict[key] == '':
                req_dict[key] = None

        #保存数据
        error= discussusedcar.createbyreq(discussusedcar, discussusedcar, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return jsonify(msg)

# 添加接口（前端）
@main_bp.route("/ershouche7de79q94/discussusedcar/add", methods=['POST'])
def ershouche7de79q94_discussusedcar_add():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取参数
        req_dict = session.get("req_dict")
        #判断用户权限
        try:
            __foreEndListAuth__=discussusedcar.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限则去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users":
                req_dict['userid']=session.get("params").get("id")

        #保存数据
        error= discussusedcar.createbyreq(discussusedcar, discussusedcar, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
            return jsonify(msg)
        else:
            msg['data'] = error
        return jsonify(msg)

# 踩、赞接口
@main_bp.route("/ershouche7de79q94/discussusedcar/thumbsup/<id_>", methods=['GET'])
def ershouche7de79q94_discussusedcar_thumbsup(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        #获取要踩赞的记录
        rets=discussusedcar.getbyid(discussusedcar, discussusedcar,id_)
        update_dict={
            "id":id_,
        }
        #加减数据
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        #更新记录
        error = discussusedcar.updatebyparams(discussusedcar, discussusedcar, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 获取详情信息（后端）
@main_bp.route("/ershouche7de79q94/discussusedcar/info/<id_>", methods=['GET'])
def ershouche7de79q94_discussusedcar_info(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = discussusedcar.getbyid(discussusedcar, discussusedcar, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= discussusedcar.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__  and  "clicknum"  in discussusedcar.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=discussusedcar.updatebyparams(discussusedcar,discussusedcar,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 获取详情信息（前端）
@main_bp.route("/ershouche7de79q94/discussusedcar/detail/<id_>", methods=['GET'])
def ershouche7de79q94_discussusedcar_detail(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = discussusedcar.getbyid(discussusedcar, discussusedcar, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= discussusedcar.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__ and "clicknum" in discussusedcar.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=discussusedcar.updatebyparams(discussusedcar,discussusedcar,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 更新接口
@main_bp.route("/ershouche7de79q94/discussusedcar/update", methods=['POST'])
def ershouche7de79q94_discussusedcar_update():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #如果存在密码或点击次数则不更新
        if req_dict.get("mima") and "mima" not in discussusedcar.__table__.columns :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in discussusedcar.__table__.columns :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass

        #更新记录
        error = discussusedcar.updatebyparams(discussusedcar, discussusedcar, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return jsonify(msg)

# 删除接口
@main_bp.route("/ershouche7de79q94/discussusedcar/delete", methods=['POST'])
def ershouche7de79q94_discussusedcar_delete():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #删除记录
        error=discussusedcar.delete(
            discussusedcar,
            req_dict
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 投票接口
@main_bp.route("/ershouche7de79q94/discussusedcar/vote/<int:id_>", methods=['POST'])
def ershouche7de79q94_discussusedcar_vote(id_):
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success"}
        #根据id获取记录
        data= discussusedcar.getbyid(discussusedcar, discussusedcar, int(id_))
        for i in data:
            #增加投票数并更新记录
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=discussusedcar.updatebyparams(discussusedcar,discussusedcar,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return jsonify(msg)




#获取所有记录列表
@main_bp.route("/ershouche7de79q94/discussusedcar/lists", methods=['GET'])
def ershouche7de79q94_discussusedcar_lists():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}
        req_dict = session.get("req_dict")
        list,_,_,_,_ = discussusedcar.page(discussusedcar,discussusedcar,req_dict)
        msg['data'] = list
        return jsonify(msg)






