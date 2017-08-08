# coding:utf-8
from flask import Blueprint,request,\
    url_for,redirect,views,g,session,\
    render_template,abort,make_response
from utils.captcha import xtcaptcha
from utils import rhjcache,alidayu_sms,xtjson
from forms.front_forms import FrontUserRegistForm,FrontLoginForm,FrontSettingForm
from decorators.front_decorators import login_required
from constants import FRONT_USER_ID
from tasks import celery_send_sms
import random

try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp=Blueprint('account',__name__,url_prefix='/account')

@bp.route('/')
def account_index():
    return 'account_index'

class Front_RegistView(views.MethodView):
    def get(self,**kw):
        context=kw
        return render_template('front/front_regist.html',**context)

    def post(self):
        form=FrontUserRegistForm(request.form)
        telephone=form.telephone.data
        username=form.username.data

        if form.validate():
            return redirect(url_for('post.post_index'))
        else:
            return self.get(message=form.get_error(),telephone=telephone,username=username)

bp.add_url_rule('/regist/',view_func=Front_RegistView.as_view('front_regist'))

class Front_LoginView(views.MethodView):
    def get(self,**kw):
        context=kw
        return render_template('front/front_login.html',**context)
    def post(self):
        form=FrontLoginForm(request.form)
        if form.validate():
            nexturl=request.args.get('next')
            if nexturl:
                return redirect(nexturl)
            else:
                return redirect(url_for('post.post_index'))
        else:
            return self.get(message=form.get_error())

bp.add_url_rule('/login/',view_func=Front_LoginView.as_view('front_login'))


@bp.route('/settings/',methods=['GET','POST'])
@login_required
def front_settings():
    if request.method=='GET':
        return render_template('front/front_settings.html')
    else:
        form=FrontSettingForm(request.form)
        if form.validate():
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


@bp.route('/logout/')
@login_required
def front_logout():
    session.pop(FRONT_USER_ID)
    return redirect(url_for('account.front_login'))


@bp.route('/sms_captcha/')
def sms_captcha():
    telephone=request.args.get('telephone')
    if not telephone:
        return xtjson.json_params_error(message='请输入邮箱')
    if rhjcache.get(telephone):
        return xtjson.json_params_error(message='已向该邮箱发送验证码,请2分钟后再试')

    text=xtcaptcha.Captcha.gene_text()
    celery_send_sms.delay(telephone=telephone,captcha=text)
    rhjcache.set(telephone,text.lower(),time=2*60)
    return xtjson.json_result()

@bp.route('/graph_captcha/')
def graph_captcha():
    text,image=xtcaptcha.Captcha.gene_code()
    out=StringIO()
    image.save(out,'png')
    out.seek(0)

    response=make_response(out.read())
    response.content_type='image/png'
    rhjcache.set(text.lower(),text.lower(),time=2*60)
    return response





# ----------------------测试函数---------------------------------------------
@bp.route('/test/')
def test():
    return render_template('front/front_sign_base.html')