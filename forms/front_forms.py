# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,DateField,ValidationError
from wtforms.validators import InputRequired,Length,URL,EqualTo,Email
from forms.base_forms import BaseForm
from models.cms_models import CMS_User
from flask import session,g
from constants import CMS_USER_ID
from exts import db
from utils import rhjcache
from utils.captcha import xtcaptcha
from models.front_models import FrontUser
from models.common_models import PostModel,HighlightModel,PostStarModel,CommentModel
from constants import FRONT_USER_ID
from datetime import datetime
from utils.xtredis import BBS_Redis

import random

class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[Length(4, 4, message=u'图片验证码格式错误'), InputRequired(message=u'图片验证码不能为空')])

    def validate_graph_captcha(self, field):
        graph_captcha = field.data.lower()
        if xtcaptcha.Captcha.check_captcha(graph_captcha):
            return True
        else:
            self.graph_captcha.errors.append(u'验证码输入有误！')
            return False

class FrontUserRegistForm(GraphCaptchaForm):
    telephone=StringField(validators=[Length(11,11,message=u'手机格式错误'),InputRequired(message=u'手机号码不能为空')])
    sms_captcha=StringField(validators=[Length(4,4,message=u'短信验证码格式错误'),InputRequired(message=u'短息验证码不能为空')])
    username=StringField(validators=[Length(3,12,message=u'用户名为3-12位字符'),InputRequired(message=u'用户名不能为空')])
    password=StringField(validators=[Length(6,20,message=u'密码长度为6-20位字符'),InputRequired(message=u'密码不能为空')])
    password_repeat=StringField(validators=[EqualTo('password',message=u'两次密码输入不一致')])

    def validate(self):
        if not super(FrontUserRegistForm, self).validate():
            return False
        else:
            telephone=self.telephone.data
            sms_captcha=self.sms_captcha.data
            username=self.username.data
            password=self.password.data

            db_user=FrontUser.query.filter_by(telephone=telephone).first()

            cache_sms=xtcaptcha.Captcha.check_captcha(telephone)
            if not cache_sms or sms_captcha!=cache_sms:
                self.sms_captcha.errors.append(u'短信验证码输入有误！')

            if db_user:
                self.telephone.errors.append(u'该手机号码已经注册！')
            user=FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return True

class FrontLoginForm(GraphCaptchaForm):
    telephone=StringField(validators=[Length(3,12,message=u'用户名或密码错误!'),InputRequired(message=u'用户名不能为空!')])
    password=StringField(validators=[Length(6,20,message=u'用户名或密码错误'),InputRequired(message=u'密码不能为空!')])
    remember=IntegerField()

    def validate(self):
        if not super(FrontLoginForm, self).validate():
            return False
        else:
            telephone=self.telephone.data
            password=self.password.data

            user=FrontUser.query.filter_by(telephone=telephone).first()

            if not user.is_active:
                self.telephone.errors.append(u'该用户已被封禁，不能登录!')
                return False

            if not user or not user.check_password(password):
                self.telephone.errors.append(u'用户名或密码错误!')
                return False
            else:
                now = datetime.now()
                if user.old_login_time:
                    user.last_login_time=user.old_login_time
                user.old_login_time=now

                if self.remember.data:
                    session.permanent=True
                session[FRONT_USER_ID]=user.id
                user.points+=random.randint(1,3)
                db.session.commit()
                return True

class FrontAddPostForm(GraphCaptchaForm):
    title=StringField(validators=[Length(3,100,message=u'标题长度为3-100字符'),InputRequired(message=u'标题不能为空!')])
    board_id=IntegerField(validators=[InputRequired(message=u'必须指定版块!')])
    content=StringField(validators=[InputRequired(message=u'内容不能为空')])

class FrontAddCommentForm(BaseForm):
    post_id=IntegerField(validators=[InputRequired(message=u'必须指定帖子ID')])
    content=StringField(validators=[InputRequired(message=u'内容不能为空')])
    origin_comment_id=IntegerField()

    def validate(self):
        if not super(FrontAddCommentForm, self).validate():
            return False

        post_id=self.post_id.data
        content=self.content.data
        origin_comment_id=self.origin_comment_id.data

        post=PostModel.query.filter_by(id=post_id).first()
        if not post:
            self.post_id.errors.append(u'没有该帖子！')

        else:
            comment=CommentModel(content=content)
            g.front_user.comments.append(comment)
            if origin_comment_id:
                origin_comment=CommentModel.query.filter_by(id=origin_comment_id).first()
                comment.origin_comment=origin_comment
            post.comments.append(comment)
            comment.author.points+=random.randint(3,5)
            db.session.commit()

            BBS_Redis.comment.active_flush(comment)

            return True

class FrontPostStarForm(BaseForm):
    post_id=IntegerField(validators=[InputRequired(message=u'必须指定帖子ID!')])
    is_star=IntegerField(validators=[InputRequired(message=u'必须指定行为!')])

    def validate(self):
        if not super(FrontPostStarForm, self).validate():
            return False
        else:
            post_id=self.post_id.data
            is_star=self.is_star.data

            post=PostModel.query.filter_by(id=post_id).first()
            if not post:
                self.post_id.errors.append(u'没有找到该贴子!')
            else:
                star_author_ids=[star.author.id for star in post.stars ]
                if g.front_user.id not in star_author_ids:
                    if is_star:
                        star=PostStarModel()
                        star.author=g.front_user
                        post.stars.append(star)
                        db.session.commit()
                        return True
                    else:
                        self.is_star.errors.append(u'您当前没有点赞,无需取消赞!')
                else:
                    if not is_star:
                        db_star=PostStarModel.query.filter_by(
                            author_id=g.front_user.id).first()
                        db.session.delete(db_star)
                        db.session.commit()
                        return True
                    else:
                        self.is_star.errors.append(u'您已经点赞，无需重复点赞!')

class FrontSettingForm(BaseForm):
    username=StringField(validators=[Length(3,12,message=u'用户名格式错误!'),InputRequired(message=u'用户名不能为空!')])
    realname=StringField()
    qq=StringField()
    avatar=StringField(validators=[URL(message=u'头像必须为URL格式!')])
    signature=StringField()

    def validate(self):
        if not super(FrontSettingForm, self).validate():
            return False
        else:
            username=self.username.data
            all_users=FrontUser.query.all()
            front_user_usernames=[i.username for i in all_users]
            if username in front_user_usernames and username!=g.front_user.username:
                return self.username.errors.append(u'该用户名不能使用，因为已存在!')



            user_dict=dict(
            username=self.username.data,
            realname=self.realname.data if self.realname.data else False,
            qq=self.qq.data if self.qq.data else False,
            avatar=self.avatar.data if self.avatar.data else False,
            signature=self.signature.data if self.signature.data else False
            )

            for i in user_dict:
                if user_dict.get(i):
                   setattr(g.front_user,i,user_dict.get(i))
            db.session.commit()
            return True



