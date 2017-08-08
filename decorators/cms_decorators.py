# coding:utf-8
from flask import session,redirect,url_for,abort,g
from functools import wraps
from constants import CMS_USER_ID
from models.cms_models import CMS_Permission

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kw):
        if session.get(CMS_USER_ID):
            return func(*args,**kw)
        else:
            return redirect(url_for('cms.cms_login'))
    return wrapper

def permission_required(permission):
    def deco(func):
        @wraps(func)
        def wrapper(*args,**kw):
            if g.cms_user.has_permission(permission):
                return func(*args,**kw)
            else:
                abort(401)
        return wrapper
    return deco


def superadmin_required(func):
    return permission_required(CMS_Permission.SUPER_ADMIN)(func)