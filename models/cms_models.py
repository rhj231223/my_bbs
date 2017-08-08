# coding:utf-8
from exts import db
from base_models import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class CMS_Permission(object):
    SUPER_ADMIN=255
    OPERATOR=1

    PERMISSION_MAP={
        255:(u'超级管理员','超级管理员拥有至高无上的权力'),
        1:(u'普通管理员','普通管理员拥有管理前台用户帖子的权力')
    }

cms_user_role=db.Table('cms_user_role',
                       db.Column('user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True),
                       db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True))


class CMS_Role(db.Model):
    __tablename__='cms_role'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    permission=db.Column(db.Integer,default=CMS_Permission.OPERATOR)


class CMS_User(db.Model,BaseModel):
    __tablename__='cms_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    join_time=db.Column(db.DateTime,default=datetime.now)
    is_active=db.Column(db.Boolean,default=True)
    last_login_time=db.Column(db.DateTime)

    roles=db.relationship('CMS_Role',secondary='cms_user_role',backref='users')


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_pwd):
        self._password=generate_password_hash(raw_pwd)

    def check_password(self,raw_pwd):
        return check_password_hash(self._password,raw_pwd)

    def has_permission(self,permission):
        if not self.roles:
            return False
        all_permission=0
        for role in self.roles:
            all_permission |=role.permission
        return permission & all_permission==permission

    @property
    def is_superadmin(self):
        return self.has_permission(CMS_Permission.SUPER_ADMIN)

    @property
    def permission(self):
        if not self.roles:
            return False
        else:
            all_permission=0
            for role in self.roles:
                all_permission|=role.permission

            permission_list=[]
            for permission,permission_info in CMS_Permission.PERMISSION_MAP.iteritems():
                if all_permission&permission==permission:
                    permission_list.append({permission:permission_info})
            return permission_list