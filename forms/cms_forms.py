# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,DateField
from wtforms.validators import InputRequired,Length,URL,EqualTo,Email
from forms.base_forms import BaseForm
from models.cms_models import CMS_User
from models.front_models import FrontUser
from flask import session,g
from constants import CMS_USER_ID
from exts import db
from utils import rhjcache
from models.common_models import BoardModel,PostModel,HighlightModel,PostStarModel

class CMSLoginForm(BaseForm):
    email=StringField(validators=[Email(message=u'格式错误'),InputRequired(message=u'必须输入邮箱')])
    password=StringField(validators=[Length(6,20,message=u'密码错误'),InputRequired(message=u'必须输入密码')])
    remember=IntegerField()

    def validate(self):
        if not super(CMSLoginForm, self).validate():
            return False
        else:
            email=self.email.data
            password=self.password.data
            remember=self.remember.data
            user=CMS_User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if not user.is_active:
                    self.email.errors.append(u'该帐号已被封锁,无法登录！')
                    return False

                if remember:
                    session.permanent = True
                session[CMS_USER_ID] =user.id
                return True
            else:
                self.email.errors.append(u'帐号或密码错误！')
                return False

class CMSResetPwdForm(BaseForm):
    old_password=StringField(validators=[Length(6,20,message=u'旧密码格式错误'),InputRequired(message=u'旧密码不能为空！')])
    new_password=StringField(validators=[Length(6,20,message=u'新密码格式错误'), InputRequired(message=u'新密码不能为空！')])
    new_password_repeat=StringField(validators=[EqualTo('new_password',message=u'两次密码输入必须一致')])

    def validate_old_password(self,field):
        old_password=field.data

        user=g.cms_user
        if user:
            if user.check_password(old_password):
                g.cms_user.password=self.new_password.data
                db.session.commit()
                return True
            else:
                self.old_password.errors.append(u'旧密码输入错误！')
                return False

class CMSResetMailForm(BaseForm):
    email=StringField(validators=[Email(message=u'邮箱格式错误!'),InputRequired(message=u'邮箱不能为空!')])
    captcha=StringField(validators=[Length(4,4,message=u'验证码错误!'),InputRequired(message=u'验证码不能为空!')])

    def validate(self):
        if not super(CMSResetMailForm, self).validate():
            return False
        else:
            email=self.email.data
            captcha=self.captcha.data.lower()
            if captcha==rhjcache.get(email):
                user=g.cms_user
                if user.email!=email:
                    user.email=email
                    db.session.commit()
                    return True
                else:
                    self.captcha.errors.append('绑定邮箱与填写邮箱一致无需修改!')
                    return False
            else:
                self.captcha.errors.append(u'验证码错误!')
                return False

class AddCMSUserForm(BaseForm):
    email=StringField(validators=[Email(message=u'邮箱格式错误!')])
    username=StringField(validators=[Length(3,12,message=u'用户名格式错误!')])
    password=StringField(validators=[Length(6,20,message=u'密码格式错误！')])


class BlackListForm(BaseForm):
    user_id=IntegerField(validators=[InputRequired(message=u'必须指定用户ID')])
    is_active=IntegerField(validators=[InputRequired(message=u'必须指定行为')])

    def validate(self):
        if not super(BlackListForm, self).validate():
            return False
        else:
            user_id=self.user_id.data
            is_active=self.is_active.data

            user=CMS_User.query.filter_by(id=user_id).first()
            if user.is_active:
                if is_active:
                    user.is_active=0
                    db.session.commit()
                    return True
                else:
                    self.is_active.errors.append(u'该用户不在黑名单中，无需取消拉黑')

            else:
                if not user.is_active:
                    if not is_active:
                        user.is_active=1
                        db.session.commit()
                        return True
                    else:
                        self.is_active.errors.append(u'该用户已拉黑，无需重复拉黑！')

class CMSEditBoardForm(BaseForm):
    board_id=IntegerField(validators=[InputRequired(message=u'必须指定版块ID!')])
    board_name=StringField(validators=[InputRequired(message=u'必须指定版块名称!')])


    def validate_board_name(self,filed):
        board_name=filed.data
        board_id = self.board_id.data
        db_board = BoardModel.query.filter_by(name=board_name).first()
        if db_board:
            self.board_name.errors.append(u'新版块名称与原版块名称一致,无需修改')
        else:
            board=BoardModel.query.filter_by(id=board_id).first()
            board.name=board_name
            db.session.commit()
            return True

class CMSHighlightForm(BaseForm):
    post_id=IntegerField(validators=[InputRequired(message=u'必须指定帖子ID')])
    is_highlight=IntegerField(validators=[InputRequired(message=u'必须指定行为')])

    def validate(self):
        if not super(CMSHighlightForm, self).validate():
            return False
        else:
            post_id=self.post_id.data
            is_highlight=self.is_highlight.data
            post=PostModel.query.filter_by(id=post_id).first()
            if not post:
                self.post_id.errors.append(u'没有找到该贴子')
            else:
                if not post.highlight:
                    if is_highlight:
                        highlight=HighlightModel()
                        post.highlight=highlight
                        db.session.commit()
                        return True
                    else:
                        self.is_highlight.errors.append(u'该贴子没有加精，无需取消！')
                else:
                    if not is_highlight:
                        db.session.delete(post.highlight)
                        db.session.commit()
                        return True
                    else:
                        self.is_highlight.errors.append(u'该贴子已经加精,无需重复加精！')

class CMSPostRemovedForm(BaseForm):
    post_id=IntegerField(validators=[InputRequired(message=u'必须指定帖子ID!')])
    is_removed=IntegerField(validators=[InputRequired(message=u'必须指定行为!')])

    def validate(self):
        if not super(CMSPostRemovedForm, self).validate():
            return False
        else:
            post_id=self.post_id.data
            is_removed=self.is_removed.data

            post=PostModel.query.filter_by(id=post_id).first()
            if not post:
                self.post_id.errors.append(u'没有该贴子')
            else:
                if not post.is_removed:
                    if is_removed:
                        post.is_removed=1
                        db.session.commit()
                        return True

                    else:
                        self.is_removed.errors.append(u'该帖子没有被移除,无需取消移除!')

                else:
                    if not is_removed:
                        post.is_removed=0
                        db.session.commit()
                        return True
                    else:
                        self.is_removed.errors.append(u'该帖子已经被移除，无需重复移除!')


class CMSBlackListF(BaseForm):
    user_id=StringField(validators=[InputRequired(message=u'必须指定用户ID!')])
    is_active=IntegerField(validators=[InputRequired(message=u'必须指定行为!')])

    def validate(self):
        if not super(CMSBlackListF, self).validate():
            return False
        else:
            user_id = self.user_id.data
            is_active = self.is_active.data

            user=FrontUser.query.filter_by(id=user_id).first()
            if not user:
                self.user_id.errors.append(u'没有找到该用户')
            else:
                if user.is_active:
                    if not is_active:
                        user.is_active=0
                        db.session.commit()
                        return True
                    else:
                        self.is_active.errors.append(u'该用户没有被拉黑，无需取消拉黑!')
                else:
                    if is_active:
                        user.is_active=1
                        db.session.commit()
                        return True
                    else:
                        self.is_active.errors.append(u'该用户已被拉黑,无需重复拉黑!')
