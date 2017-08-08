# coding:utf-8
import os
import pymysql
from datetime import timedelta
SECRET_KEY=os.urandom(24)

USERNAME='root'
PASSWORD='2312231223'

HOSTNAME='127.0.0.1'
PORT='3306'

DATABASE='my_bbs'
CHARSET='charset=utf8'


DB_URI='mysql+pymysql://{}:{}@{}:{}/{}?{}' .format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE,CHARSET)

SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=False


PERMANENT_SESSION_LIFETIME=timedelta(days=90)

SERVER_NAME='my_bbs.com:7000'


MAIL_SERVER='smtp.qq.com'
MAIL_PORT='587'

MAIL_USERNAME='657930342@qq.com'
MAIL_PASSWORD='aerwnvktnjhzbfib'

MAIL_DEFAULT_SENDER='657930342@qq.com'
MAIL_USE_TLS=True

