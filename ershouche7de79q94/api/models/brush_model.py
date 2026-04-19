# coding:utf-8
import random
from datetime import datetime
from sqlalchemy import text,TIMESTAMP

from api.models.models import Base_model
from api.exts import db
from sqlalchemy.dialects.mysql import DOUBLE,LONGTEXT
# 个人信息
class yonghu(Base_model):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='zhanghao'


    __authTables__={}
    __authPeople__ = '是'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    zhanghao=db.Column( db.VARCHAR(255), nullable=False,unique=True,comment='账号' )
    mima=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='密码' )
    xingming=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='姓名' )
    xingbie=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='性别' )
    touxiang=db.Column( db.Text, nullable=False, unique=False,comment='头像' )
    nianling=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='年龄' )
    shenfenzheng=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='身份证' )
    mobile=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='手机号' )

class usedcar(Base_model):
    __doc__ = u'''usedcar'''
    __tablename__ = 'usedcar'



    __authTables__={}
    __authPeople__ = '否'
    __authSeparate__='否'
    __thumbsUp__='是'
    __intelRecom__='用协'
    __browseClick__='是'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    brand=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='品牌' )
    model1=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='型号' )
    discountprice=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='现价' )
    originalprice=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='已减' )
    vehicleage=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='年份' )
    kilometer=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='行驶里程' )
    imgurl=db.Column( db.Text,  nullable=True, unique=False,comment='图片' )
    xqurl=db.Column( db.Text,  nullable=True, unique=False,comment='链接' )
    city=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='所在城市' )
    thumbsupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='赞' )
    crazilynum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='踩' )
    clicktime=db.Column( db.DateTime,  nullable=True, unique=False,comment='最近点击时间' )
    clicknum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='点击次数' )
    discussnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='评论数' )
    storeupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='收藏数' )

class usedcarforecast(Base_model):
    __doc__ = u'''usedcarforecast'''
    __tablename__ = 'usedcarforecast'



    __authTables__={}
    __authPeople__ = '否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    brand=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='品牌' )
    model1=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='型号' )
    discountprice=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='现价' )
    vehicleage=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='年份' )
    kilometer=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='行驶里程' )
    city=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='所在城市' )

class news(Base_model):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    __authPeople__ = '否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    introduction=db.Column( db.Text,  nullable=True, unique=False,comment='简介' )
    picture=db.Column( db.Text, nullable=False, unique=False,comment='图片' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )
    name=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='发布人' )
    headportrait=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )

class storeup(Base_model):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    userid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='用户id' )
    refid=db.Column( db.BigInteger, default=0 ,  nullable=True, unique=False,comment='商品id' )
    tablename=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='表名' )
    name=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='名称' )
    picture=db.Column( db.Text,  nullable=True, unique=False,comment='图片' )
    type=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='类型' )
    inteltype=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='推荐类型' )
    remark=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='备注' )

class systemintro(Base_model):
    __doc__ = u'''systemintro'''
    __tablename__ = 'systemintro'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    subtitle=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='副标题' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )
    picture1=db.Column( db.Text,  nullable=True, unique=False,comment='图片1' )
    picture2=db.Column( db.Text,  nullable=True, unique=False,comment='图片2' )
    picture3=db.Column( db.Text,  nullable=True, unique=False,comment='图片3' )

class smsregistercode(Base_model):
    __doc__ = u'''smsregistercode'''
    __tablename__ = 'smsregistercode'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    mobile=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='手机' )
    role=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='角色' )
    code=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='验证码' )

class users(Base_model):
    __doc__ = u'''users'''
    __tablename__ = 'users'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    username=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='用户名' )
    password=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='密码' )
    role=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='角色' )
    image=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )

class discussusedcar(Base_model):
    __doc__ = u'''discussusedcar'''
    __tablename__ = 'discussusedcar'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    refid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='关联表id' )
    userid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='用户id' )
    avatarurl=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    nickname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='用户名' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='评论内容' )
    reply=db.Column( db.Text,  nullable=True, unique=False,comment='回复内容' )
    thumbsupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='赞' )
    crazilynum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='踩' )
    istop=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='置顶(1:置顶,0:非置顶)' )
    tuserids=db.Column( db.Text,  nullable=True, unique=False,comment='赞用户ids' )
    cuserids=db.Column( db.Text,  nullable=True, unique=False,comment='踩用户ids' )

