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
import pandas as pd
# 分类接口（后端）
@main_bp.route("/ershouche7de79q94/usedcar/page", methods=['GET'])
def ershouche7de79q94_usedcar_page():
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
        msg['data']['pageSize']  = usedcar.page(usedcar, usedcar, req_dict, or_clauses)
        return jsonify(msg)


# 排序接口
@main_bp.route("/ershouche7de79q94/usedcar/autoSort", methods=['GET'])
def ershouche7de79q94_usedcar_autosort():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        req_dict['sort']='clicktime'
        req_dict['order']='desc'

        try:#获取需要排序的内容
            __browseClick__= usedcar.__browseClick__
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
        msg['data']['pageSize']  = usedcar.page(usedcar, usedcar, req_dict)

        return jsonify(msg)

#查询单条数据
@main_bp.route("/ershouche7de79q94/usedcar/query", methods=['GET'])
def ershouche7de79q94_usedcar_query():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{}}
        #获取传递的参数，根据参数获取单条结果
        req_dict = session.get("req_dict")
        query = db.session.query(usedcar)
        for key, value in req_dict.items():
            query = query.filter(getattr(usedcar, key) == value)
        query_result = query.first()
        query_result.__dict__.pop('_sa_instance_state', None)
        msg['data'] = query_result.__dict__
        return jsonify(msg)

# 分页接口（前端）
@main_bp.route("/ershouche7de79q94/usedcar/list", methods=['GET'])
def ershouche7de79q94_usedcar_list():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']

        userinfo = session.get("params")

        try:#判断是否有列表权限
            __foreEndListAuth__=usedcar.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限判断就去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None:
                req_dict['userid']=session.get("params").get("id")
        tablename=session.get("tablename")
        if 'luntan' in 'usedcar':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        if 'discuss' in 'usedcar':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        #根据封装的req_dict字典去筛选获取列表数据
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = usedcar.page(usedcar, usedcar, req_dict)
        return jsonify(msg)

# 保存接口（后端）
@main_bp.route("/ershouche7de79q94/usedcar/save", methods=['POST'])
def ershouche7de79q94_usedcar_save():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        for key in req_dict:#将空值转为None
            if req_dict[key] == '':
                req_dict[key] = None

        #保存数据
        error= usedcar.createbyreq(usedcar, usedcar, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return jsonify(msg)

# 添加接口（前端）
@main_bp.route("/ershouche7de79q94/usedcar/add", methods=['POST'])
def ershouche7de79q94_usedcar_add():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取参数
        req_dict = session.get("req_dict")
        #判断用户权限
        try:
            __foreEndListAuth__=usedcar.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限则去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users":
                req_dict['userid']=session.get("params").get("id")

        #保存数据
        error= usedcar.createbyreq(usedcar, usedcar, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
            return jsonify(msg)
        else:
            msg['data'] = error
        return jsonify(msg)

# 踩、赞接口
@main_bp.route("/ershouche7de79q94/usedcar/thumbsup/<id_>", methods=['GET'])
def ershouche7de79q94_usedcar_thumbsup(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        #获取要踩赞的记录
        rets=usedcar.getbyid(usedcar, usedcar,id_)
        update_dict={
            "id":id_,
        }
        #加减数据
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        #更新记录
        error = usedcar.updatebyparams(usedcar, usedcar, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 获取详情信息（后端）
@main_bp.route("/ershouche7de79q94/usedcar/info/<id_>", methods=['GET'])
def ershouche7de79q94_usedcar_info(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = usedcar.getbyid(usedcar, usedcar, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= usedcar.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__  and  "clicknum"  in usedcar.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=usedcar.updatebyparams(usedcar,usedcar,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 获取详情信息（前端）
@main_bp.route("/ershouche7de79q94/usedcar/detail/<id_>", methods=['GET'])
def ershouche7de79q94_usedcar_detail(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = usedcar.getbyid(usedcar, usedcar, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= usedcar.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__ and "clicknum" in usedcar.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=usedcar.updatebyparams(usedcar,usedcar,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 更新接口
@main_bp.route("/ershouche7de79q94/usedcar/update", methods=['POST'])
def ershouche7de79q94_usedcar_update():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #如果存在密码或点击次数则不更新
        if req_dict.get("mima") and "mima" not in usedcar.__table__.columns :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in usedcar.__table__.columns :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass

        #更新记录
        error = usedcar.updatebyparams(usedcar, usedcar, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return jsonify(msg)

# 删除接口
@main_bp.route("/ershouche7de79q94/usedcar/delete", methods=['POST'])
def ershouche7de79q94_usedcar_delete():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #删除记录
        error=usedcar.delete(
            usedcar,
            req_dict
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 投票接口
@main_bp.route("/ershouche7de79q94/usedcar/vote/<int:id_>", methods=['POST'])
def ershouche7de79q94_usedcar_vote(id_):
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success"}
        #根据id获取记录
        data= usedcar.getbyid(usedcar, usedcar, int(id_))
        for i in data:
            #增加投票数并更新记录
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=usedcar.updatebyparams(usedcar,usedcar,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return jsonify(msg)

#分组统计接口
@main_bp.route("/ershouche7de79q94/usedcar/group/<columnName>", methods=['GET'])
def ershouche7de79q94_usedcar_group(columnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        limit = 0
        order = ""
        if "limit" in req_dict:
            limit = req_dict["limit"]
            del req_dict["limit"]
        if "order" in req_dict:
            order = req_dict["order"]
            del req_dict["order"]
        userinfo = session.get("params")
        #获取hadoop分析后的数据文件
        json_filename = f'usedcar_group{columnName}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            between_params = {}
            if req_dict.get("conditionColumn") is not None:
                for index,value in enumerate(req_dict.get("conditionColumn").split(";")):
                    if "," in value:
                        between_params[value] = req_dict.get("conditionValue").split(";")[index]
                    else:
                        req_dict[value] = req_dict.get("conditionValue").split(";")[index]
                del req_dict["conditionColumn"]
                del req_dict["conditionValue"]
            #查询记录
            msg['data'] = usedcar.groupbycolumnname(usedcar,usedcar,columnName,req_dict,between_params)
            msg['data'] = msg['data'][:10]
            msg['data'] = [ {**i,columnName:str(i[columnName])} if columnName in i else i for i in msg['data']]
        #对结果进行升序可降序排序
        if order == "desc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
        elif order == "asc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])
        #截取列表个数
        if 0 < int(limit) < len(msg['data']):
            msg['data'] = msg['data'][:int(limit)]
        return jsonify(msg)#返回封装的json结果

# 按值统计接口
@main_bp.route("/ershouche7de79q94/usedcar/value/<xColumnName>/<yColumnName>", methods=['GET'])
def ershouche7de79q94_usedcar_value(xColumnName, yColumnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取参数
        req_dict = session.get("req_dict")
        limit = 0
        order = ""
        if "limit" in req_dict:
            limit = req_dict["limit"]
            del req_dict["limit"]
        if "order" in req_dict:
            order = req_dict["order"]
            del req_dict["order"]
        userinfo = session.get("params")
        #获取hadoop分析后的数据文件
        json_filename = f'usedcar_value{xColumnName}{yColumnName}.json'
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            between_params = {}
            if req_dict.get("conditionColumn") is not None:
                for index,value in enumerate(req_dict.get("conditionColumn").split(";")):
                    if "," in value:
                        between_params[value] = req_dict.get("conditionValue").split(";")[index]
                    else:
                        req_dict[value] = req_dict.get("conditionValue").split(";")[index]
                del req_dict["conditionColumn"]
                del req_dict["conditionValue"]
                #查询记录
            msg['data'] = usedcar.getvaluebyxycolumnname(usedcar,usedcar,xColumnName,yColumnName,req_dict,between_params)
        #对结果进行升序可降序排序
        if order == "desc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
        elif order == "asc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])
        #截取列表个数
        if 0 < int(limit) < len(msg['data']):
            msg['data'] = msg['data'][:int(limit)]
        return jsonify(msg)#返回封装的json结果

#对日期进行排序
def order_time(data,type,xColumnName,rev):
    if type=="日":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),
                int(x[xColumnName].split("-")[1]),
                int(x[xColumnName].split("-")[2]),
            ),
            reverse=rev  # 设置排列
        )
    elif type=="月":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),
                int(x[xColumnName].split("-")[1])
            ),
            reverse=rev  # 设置排列
        )
    elif type=="年":
        result_data = sorted(
            data,
            key=lambda x: (
                int(x[xColumnName].split("-")[0]),  # 提取年份并转为整数
            ),
            reverse=rev  # 设置排列
        )
    else:
        result_data = sorted(data, key=lambda x: x[xColumnName], reverse=rev)
    return result_data

# 按日期统计接口
@main_bp.route("/ershouche7de79q94/usedcar/value/<xColumnName>/<yColumnName>/<timeStatType>", methods=['GET'])
def ershouche7de79q94_usedcar_value_riqi(xColumnName, yColumnName, timeStatType):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"
        json_filename = f'usedcar_value{xColumnName}{yColumnName}{date_type}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            if req_dict.get("conditionColumn") is not None:
                for index, value in enumerate(req_dict.get("conditionColumn").split(";")):
                    if ',' in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{req_dict.get("conditionValue").split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{req_dict.get("conditionValue").split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{req_dict.get("conditionValue").split(";")[index]}\''''
                del req_dict["conditionColumn"]
                del req_dict["conditionValue"]
            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
            #定义查询统计语句
            for key, value in req_dict.items():
                if key!="limit" and key!="order" and key!="orderType":
                    where = where + " and {0} ='{1}' ".format(key,value)
            sql = ''
            if timeStatType == '日':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName,statistics_func,yColumnName, where, '%Y-%m-%d')
            if timeStatType == '月':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, statistics_func,yColumnName, where, '%Y-%m')
            if timeStatType == '季':
                sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) AS {0}, {1}({2}) AS total FROM orders {3} GROUP BY YEAR({0}), QUARTER({0})".format(xColumnName, statistics_func,yColumnName, where)
            if timeStatType == '年':
                sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, statistics_func,yColumnName, where, '%Y')
            #执行查询
            data = db.session.execute(sql)
            data = data.fetchall()
            #封装结果
            results = []
            for i in range(len(data)):
                result = {
                    xColumnName: decimalEncoder(data[i][0]),
                    'total': decimalEncoder(data[i][1])
                }
                results.append(result)

            msg['data'] = results
            json_filename='usedcar'+f'_value_{xColumnName}_{yColumnName}.json'
            app.executor.submit(spark_read_mysql, f"({sql}) "+'usedcar', json_filename)
            with open(json_filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(results, indent=4, ensure_ascii=False))
            app.executor.submit(upload_to_hdfs, json_filename)
            app.executor.submit(MRMySQLAvg.run)
        #结果进行排序
        req_dict = session.get("req_dict")
        #对结果进行排序
        order = req_dict.get('order')
        orderType = req_dict.get('orderType')
        if orderType=='x' :
            if order == "desc":
                msg['data'] = order_time(msg['data'], timeStatType, xColumnName, True)
            else:
                msg['data'] = order_time(msg['data'], timeStatType, xColumnName, False)
        else:
            if order == "desc":
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None), key=lambda x: x['total'],
                                     reverse=True)
            else:
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None), key=lambda x: x['total'])

        #截取列表个数
        if "limit" in req_dict and int(req_dict["limit"]) < len(msg['data']):
            msg['data'] = msg['data'][:int(req_dict["limit"])]
        return jsonify(msg)#返回封装的json结果

# 按值统计（多）
@main_bp.route("/ershouche7de79q94/usedcar/valueMul/<xColumnName>", methods=['GET'])
def ershouche7de79q94_usedcar_valueMul(xColumnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        json_filename = f'''usedcar_value{xColumnName}{req_dict['yColumnNameMul'].replace(",","")}.json'''
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            if req_dict.get("conditionColumn") is not None:
                for index, value in enumerate(req_dict.get("conditionColumn").split(";")):
                    if ',' in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{req_dict.get("conditionValue").split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{req_dict.get("conditionValue").split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{req_dict.get("conditionValue").split(";")[index]}\''''
                del req_dict["conditionColumn"]
                del req_dict["conditionValue"]

            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
            for item in req_dict['yColumnNameMul'].split(','):
                #定义查询语句
                sql = "SELECT {0}, {1}({2}) AS total FROM usedcar {3} GROUP BY {0}".format(xColumnName, statistics_func,item, where)
                L = []
                #执行查询
                data = db.session.execute(sql)
                data = data.fetchall()
                for i in range(len(data)):
                    result = {
                        xColumnName: decimalEncoder(data[i][0]),
                        'total': decimalEncoder(data[i][1])
                    }
                    L.append(result)
                msg['data'].append(L)
        return jsonify(msg)

# 按值统计（多）
@main_bp.route("/ershouche7de79q94/usedcar/valueMul/<xColumnName>/<timeStatType>", methods=['GET'])
def ershouche7de79q94_usedcar_valueMul_time(xColumnName,timeStatType):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"

        json_filename = f'''usedcar_value{xColumnName}{req_dict['yColumnNameMul'].replace(",","")}{date_type}.json'''

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            if req_dict.get("conditionColumn") is not None:
                for index, value in enumerate(req_dict.get("conditionColumn").split(";")):
                    if ',' in value:
                        where = where + f''' and {value.split(',')[0]} >= \'{req_dict.get("conditionValue").split(";")[index].split(",")[0]}\''''
                        where = where + f''' and {value.split(',')[1]} <= \'{req_dict.get("conditionValue").split(";")[index].split(",")[1]}\''''
                    else:
                        where = where + f''' and {value} = \'{req_dict.get("conditionValue").split(";")[index]}\''''
                del req_dict["conditionColumn"]
                del req_dict["conditionValue"]
            statistics_func = "SUM"
            func_params = req_dict.get("func")
            if func_params == "平均":
                statistics_func = "AVG"
            elif func_params == "最大":
                statistics_func = "MAX"
            elif func_params == "最小":
                statistics_func = "MIN"
            elif func_params == "总和":
                statistics_func = "COUNT"
            try:
                del req_dict["func"]
            except:
                pass
                # 定义查询统计语句
            for key, value in req_dict.items():
                if key != "limit" and key != "order" and key != "orderType" and key != "yColumnNameMul":
                    where = where + " and {0} ='{1}' ".format(key, value)

            for item in req_dict['yColumnNameMul'].split(','):
                #定义查询语句
                sql = ''
                if timeStatType == '日':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d') ".format(xColumnName, statistics_func,item, where, '%Y-%m-%d')

                if timeStatType == '月':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y-%m') ".format(xColumnName, statistics_func,item, where, '%Y-%m')

                if timeStatType == '季':
                    sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) {0}, {1}({2}) total FROM usedcar {3} GROUP BY YEAR({0}), QUARTER({0}) ".format(xColumnName,statistics_func, item, where)

                if timeStatType == '年':
                    sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, {1}({2}) total FROM usedcar {3} GROUP BY DATE_FORMAT({0}, '%Y') ".format(xColumnName,statistics_func, item, where, '%Y')
                L = []
                #执行查询
                data = db.session.execute(sql)
                data = data.fetchall()
                for i in range(len(data)):
                    result = {
                        xColumnName: decimalEncoder(data[i][0]),
                        'total': decimalEncoder(data[i][1])
                    }
                    L.append(result)
                    # 结果进行排序
                    req_dict = session.get("req_dict")
                    order = req_dict.get('order')
                    orderType = req_dict.get('orderType')
                    if orderType == 'x':
                        if order == "desc":
                            L = order_time(L, timeStatType, xColumnName, True)
                        else:
                            L = order_time(L, timeStatType, xColumnName, False)
                    else:
                        if order == "desc":
                            L = sorted((x for x in L if x['total'] is not None),
                                       key=lambda x: x['total'],
                                       reverse=True)
                        else:
                            L = sorted((x for x in L if x['total'] is not None),
                                       key=lambda x: x['total'])
                    # 截取列表个数
                    if "limit" in req_dict and int(req_dict["limit"]) < len(msg['data']):
                        L = L[:int(req_dict["limit"])]
                msg['data'].append(L)
        return jsonify(msg)

import math
#计算相似度
def cosine_similarity(a, b):
    numerator = sum([a[key] * b[key] for key in a if key in b])
    denominator = math.sqrt(sum([a[key]**2 for key in a])) * math.sqrt(sum([b[key]**2 for key in b]))
    return numerator / denominator

#协同算法
@main_bp.route("/ershouche7de79q94/usedcar/autoSort2", methods=['GET'])
def ershouche7de79q94_usedcar_autoSort2():
    if request.method == 'GET':#get请求
        user_ratings = {}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")

        user_items = defaultdict(list)
        for userid, refid in db.session.query(storeup.userid, storeup.refid).filter(storeup.tablename == 'usedcar',storeup.type ==  1 ).distinct():
            user_items[userid].append(refid)
        for userid, refid in db.session.query(storeup.userid, storeup.refid).filter(storeup.tablename == 'usedcar',storeup.type == 21).distinct():
            user_items[userid].append(refid)
        #封装userid、goodid的矩阵
        for user, items in user_items.items():
            ratings_dict = {}
            if user_ratings.__contains__(user):
                ratings_dict=user_ratings[user]
            else:
                for item in items:
                    if ratings_dict.__contains__(str(item)):
                        ratings_dict[str(item)] += 1
                    else:
                        ratings_dict[str(item)] =1
            user_ratings[user] = ratings_dict
        sorted_recommended_goods=[]
        try:
            # 计算目标用户与其他用户的相似度
            similarities = {other_user: cosine_similarity(user_ratings[userinfo.get("id")], user_ratings[other_user])
                            for other_user in user_ratings if other_user != userinfo.get("id")}
            # 找到与目标用户最相似的用户
            most_similar_user = sorted(similarities, key=similarities.get, reverse=True)[0]
            # 找到最相似但目标用户未购买过的商品
            recommended_goods = {goods: rating for goods, rating in user_ratings[most_similar_user].items() if
                                 goods not in user_ratings[userinfo.get("id")]}
            # 按评分降序排列推荐
            sorted_recommended_goods = sorted(recommended_goods, key=recommended_goods.get, reverse=True)
        except:
            pass
        L = []

        #按评分顺序查询要推荐列表(当前用户未购买过的同类型优先)
        where = " AND ".join([f"{key} = '{value}'" for key, value in req_dict.items() if key!="page" and key!="limit" and key!="order"and key!="sort"])
        if where:
            sql = f'''SELECT * FROM (SELECT * FROM usedcar WHERE {where}) AS table1 WHERE id IN ('{"','".join(sorted_recommended_goods)}') union all SELECT * FROM (SELECT * FROM usedcar WHERE {where}) AS table1 WHERE id NOT IN ('{"','".join(sorted_recommended_goods)}')  ORDER BY FIELD(id,'{"','".join(sorted_recommended_goods)}')= 0,FIELD(id,'{"','".join(sorted_recommended_goods)}')'''
        else:
            sql = f'''SELECT * FROM usedcar WHERE id IN ('{"','".join(sorted_recommended_goods)}') union all SELECT * FROM usedcar WHERE id NOT IN ('{"','".join(sorted_recommended_goods)}')  ORDER BY FIELD(id,'{"','".join(sorted_recommended_goods)}')= 0,FIELD(id,'{"','".join(sorted_recommended_goods)}')'''
        #执行查询
        data = db.session.execute(sql)
        #封装结果
        data_dict = [dict(zip(result.keys(), result)) for result in data.fetchall()]
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                elif 'datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)
        #返回封装的json结果
        return jsonify({"code": 0, "msg": '',  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":5,"list": L[0:int(req_dict['limit'])]}})


#查询记录总数量接口
@main_bp.route("/ershouche7de79q94/usedcar/count", methods=['GET'])
def ershouche7de79q94_usedcar_count():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data": 0}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")

        #查询记录个数
        msg['data']  = usedcar.count(usedcar, usedcar, req_dict)
        #返回json结果
        return jsonify(msg)


#获取所有记录列表
@main_bp.route("/ershouche7de79q94/usedcar/lists", methods=['GET'])
def ershouche7de79q94_usedcar_lists():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}
        req_dict = session.get("req_dict")
        list,_,_,_,_ = usedcar.page(usedcar,usedcar,req_dict)
        msg['data'] = list
        return jsonify(msg)

import math
#数据清洗接口
@main_bp.route("/ershouche7de79q94/usedcar/cleanse", methods=['GET','POST'])
def ershouche7de79q94_usedcar_cleanse():
    if request.method == 'GET' or request.method == 'POST':
        msg = {'code': normal_code, 'message': 'success', 'data': {}}
        try:
            #获取要清理的数据列表
            list, _,_,total,_ = usedcar.page(usedcar, usedcar,{})
            df = pd.DataFrame(list,dtype=object)
            #随机填充
            df['brand'].replace([None, '' ], pd.NA,inplace = True)
            brand_non_na = df['brand'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'brand']):
                    df.loc[i, 'brand'] = brand_non_na.sample(n=1,replace=True).values[0]
            #将DataFrame 转换为列表
            data_list = df.to_dict(orient='records')
            db.session.query(usedcar).delete()
            for dl in data_list:
                filtered_data = {k: v for k, v in dl.items() if v not in [None, '', float('nan')] and (not isinstance(v, float) or not math.isnan(v))}
                db.session.add(usedcar(**filtered_data))
            db.session.commit()
            return jsonify(msg)
        except Exception as e:
            msg["code"] = other_code
            msg["message"] = e.__str__()
            return jsonify(msg)





