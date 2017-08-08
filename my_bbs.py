#coding:utf-8
from flask import Flask,Blueprint,url_for,session,\
    g,request,render_template
import flask
from flask_wtf import CSRFProtect
from exts import app
from views.cms_views import cms_views
from views.front_views import front_account_views,front_post_views
from utils import xtjson
from constants import FRONT_USER_ID
from models.front_models import FrontUser
from datetime import datetime
from utils.xtredis import BBS_Redis

app.debug = True

CSRFProtect(app)

app.register_blueprint(cms_views.bp)
app.register_blueprint(front_account_views.bp)
app.register_blueprint(front_post_views.bp)



@app.route('/')
def hello_world():
    return 'Hello World!'







# --------------------------钩子函数-----------------------
@app.template_filter('time_handler')
def time_handler(time):
    if isinstance(time,datetime):
        now=datetime.now()
        timestamp=(now-time).total_seconds()
        time_dict={
            60:u'刚刚好',
            60*60:u'%s分钟前' %int(timestamp//60),
            60*60*24:u'%s小时前' %int(timestamp//(60*60)),
            60*60*24*30:u'%s天前' %int(timestamp//(60*60*24)),
        }
        for i in time_dict:
            if timestamp <int(i):
                return time_dict.get(i)
        if now.year==time.year:
            return time.strftime('%m-%d %H:%M:%S')
        return time.strftime('%Y-%m-%d %H:%M:%S')
    return time

@app.before_request
def add_session_to_g():
    front_user_id=session.get(FRONT_USER_ID)
    if front_user_id:
        front_user=FrontUser.query.filter_by(id=front_user_id).first()
        if front_user:
            g.front_user=front_user

@app.context_processor
def add_g_to_template():
    if hasattr(g,'front_user'):
        return dict(front_user=g.front_user)
    else:
        return {}

@app.errorhandler(401)
def unpath_forbidden(error):
    if request.is_xhr:
        return xtjson.json_unpath_error('错误401,您的权限不足')
    else:
        return render_template('common/common_401.html'),401

@app.errorhandler(404)
def page_not_found(error):
    if request.is_xhr:
        return xtjson.json_unpath_error('错误404,您访问的页面未找到')
    else:
        return render_template('common/common_404.html'),404






if __name__ == '__main__':


    app.run()