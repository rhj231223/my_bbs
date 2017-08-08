# coding:utf-8
from exts import db
from shortuuid import uuid
from models.base_models import BaseModel
from datetime import datetime
from flask import url_for
from werkzeug.security import generate_password_hash,check_password_hash


class GenderType(object):
    MAN=1
    WOMAN=2
    SELECT=3
    UNKNOWN=4


class FrontUser(db.Model,BaseModel):
    __tablename__='front_user'
    id=db.Column(db.String(100),primary_key=True,default=uuid)
    telephone=db.Column(db.String(11),nullable=False,unique=True)
    username=db.Column(db.String(100),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True)
    join_time=db.Column(db.DateTime,default=datetime.now)
    is_active=db.Column(db.Boolean,default=True)
    old_login_time=db.Column(db.DateTime)
    last_login_time=db.Column(db.DateTime)
    qq=db.Column(db.String(20))
    realname=db.Column(db.String(20))
    gender=db.Column(db.Integer,default=GenderType.SELECT)
    signature=db.Column(db.String(100))
    points=db.Column(db.Integer,default=0)
    avatar=db.Column(db.String(200),default='http://ori2rm8ly.bkt.clouddn.com/logo.jpg')

    def __init__(self,telephone,username,password):
        self.telephone=telephone
        self.username=username
        self.password=password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_pwd):
        self._password=generate_password_hash(raw_pwd)

    def check_password(self,raw_pwd):
        return check_password_hash(self.password,raw_pwd)