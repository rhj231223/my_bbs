# coding:utf-8
from flask import session,redirect,render_template,\
    request,url_for
from constants import FRONT_USER_ID
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get(FRONT_USER_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('account.front_login',next=request.path))
    return wrapper