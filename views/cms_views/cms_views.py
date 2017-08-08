# coding:utf-8
from flask import Flask,Blueprint,g,\
    session,url_for,redirect,views,render_template,\
    request,abort
from constants import CMS_USER_ID
from models.cms_models import CMS_User,CMS_Role
from forms.cms_forms import CMSLoginForm,CMSResetPwdForm,\
    CMSResetMailForm,AddCMSUserForm,BlackListForm,CMSEditBoardForm,\
    CMSHighlightForm,CMSPostRemovedForm,CMSBlackListF
from utils import xtjson
from decorators.cms_decorators import login_required,superadmin_required
from utils import xtmail,rhjcache
from utils.captcha import xtcaptcha
from exts import db
from models.common_models import BoardModel,PostModel,PostStarModel,\
    HighlightModel,CommentModel
from models.front_models import FrontUser
from models.model_helper import PostModelHelper
from tasks import celery_send_email

bp=Blueprint('cms',__name__,subdomain='cms')

# cms首页
@bp.route('/')
@login_required
def cms_index():
    return render_template('cms/cms_base.html')

@bp.route('/profile/')
@login_required
def cms_profile():
    return render_template('cms/cms_profile.html')

@bp.route('/reset_pwd/',methods=['GET','POST'])
@login_required
def cms_reset_pwd():
    if request.method=='GET':
        return render_template('cms/cms_reset_pwd.html')

    else:
        form=CMSResetPwdForm(request.form)
        if form.validate():
            return xtjson.json_result(message=u'恭喜密码修改成功！')
        else:
            return xtjson.json_params_error(message=form.get_error())

@bp.route('/reset_email/',methods=['GET','POST'])
@login_required
def cms_reset_email():
    if request.method=='GET':
        return render_template('cms/cms_reset_email.html')
    else:
        form=CMSResetMailForm(request.form)
        if form.validate():
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

@bp.route('/get_capthca/')
@login_required
def get_captcha():
    email=request.args.get('email')
    captcha=xtcaptcha.Captcha.gene_text()
    rhjcache.set(email,captcha.lower())

    celery_send_email.delay(subject='侃侃而坛验证码',receivers=[email],body=u'您的验证码:%s 有效期为2分钟' %captcha)
    return xtjson.json_result(message=u'邮件发送成功')



@bp.route('/cms_users/')
@login_required
@superadmin_required
def cms_cmsusers():
    all_users=CMS_User.query.all()
    context=dict(all_users=all_users)
    return render_template('cms/cms_cmsusers.html',**context)

@bp.route('/add_cmsuser/',methods=['GET','POST'])
@login_required
@superadmin_required
def cms_addcmsuser():
    if request.method=='GET':
        roles=CMS_Role.query.all()
        context=dict(roles=roles)
        return render_template('cms/cms_addcmsuser.html',**context)
    else:
        form=AddCMSUserForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            roles=request.form.getlist('roles[]')

            db_user=CMS_User.query.filter_by(email=email).first()
            if not db_user:
                user=CMS_User(email=email,username=username,password=password)
                if roles:
                    for role_id in roles:
                        role=CMS_Role.query.filter_by(id=role_id).first()
                        user.roles.append(role)
                    db.session.add(user)
                    db.session.commit()
                    return xtjson.json_result()
                else:
                    return xtjson.json_params_error(message=u'必须选择一个分组')

            else:
                return xtjson.json_params_error(message=u'该邮箱已注册!')

        else:
            return xtjson.json_params_error(message=form.get_error())

@bp.route('/edit_cmsuser/',methods=['GET','POST'])
@login_required
@superadmin_required
def cms_edit_cmsuser():

    if request.method=='GET':
        user_id = request.args.get('user_id')
        user = CMS_User.query.filter_by(id=user_id).first()

        roles=CMS_Role.query.all()
        if user:
            context=dict(roles=roles,user=user)
            return render_template('cms/cms_edit_cmsuser.html',**context)
        else:
            abort(404)

    else:
        role_ids=request.form.getlist('roles[]')
        user_id = request.form.get('user_id')
        user = CMS_User.query.filter_by(id=user_id).first()
        user_role_ids=[role.id for role in user.roles]

        if role_ids:
            if role_ids and role_ids == user_role_ids:
                return xtjson.json_params_error(message=u'原信息与提交信息一致,无需修改')
            else:
                user.roles=[]
                for role_id in role_ids:
                    role=CMS_Role.query.filter_by(id=role_id).first()
                    user.roles.append(role)
                db.session.commit()
                return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=u'必须选择一个分组')

@bp.route('/blacklist/',methods=['POST'])
@login_required
def blacklist():
    form=BlackListForm(request.form)
    if form.validate():
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(form.get_error())

@bp.route('/cms_posts/')
@login_required
def cms_posts():
    page=request.args.get('page',type=int,default=1)
    sort=request.args.get('sort',type=int,default=1)
    board_id=request.args.get('board_id',type=int,default=0)
    all=request.args.get('all',type=int,default=1)
    context=PostModelHelper.post_list(
        page=page,sort=sort,board_id=board_id,all=all
    )
    return render_template('cms/cms_posts.html',**context)

@bp.route('/highlight/',methods=['POST'])
@login_required
def highlight():
    form=CMSHighlightForm(request.form)
    if form.validate():
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


@bp.route('/post_removed/',methods=['POST'])
@login_required
def post_removed():
    form=CMSPostRemovedForm(request.form)
    if form.validate():
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())




# cms登录页面
class CMS_LoginView(views.MethodView):
    def get(self,message=None):
        context=dict(message=message)
        return render_template('cms/cms_login.html',**context)

    def post(self):
        form=CMSLoginForm(request.form)
        if form.validate():
            return redirect(url_for('cms.cms_index'))
        else:

            return self.get(message=form.get_error())


bp.add_url_rule('/login/',view_func=CMS_LoginView.as_view('cms_login'))

@bp.route('/cms_logout/')
@login_required
def cms_logout():
    session.pop(CMS_USER_ID)
    return redirect(url_for('cms.cms_login'))

@bp.route('/boards/')
@login_required
def cms_boards():
    boards=BoardModel.query.all()
    context=dict(boards=boards)
    return render_template('cms/cms_boards.html',**context)

@bp.route('/add_board/',methods=['POST'])
@login_required
def add_board():
    board_name=request.form.get('board_name')
    db_board=BoardModel.query.filter_by(name=board_name).first()
    if db_board:
        return xtjson.json_params_error(message=u'该板块已存在，无需添加')
    else:
        board=BoardModel(name=board_name)
        g.cms_user.boards.append(board)
        db.session.commit()
        return xtjson.json_result()

@bp.route('/edit_board/',methods=['POST'])
@login_required
def edit_board():
    form=CMSEditBoardForm(request.form)
    board_id=form.board_id.data
    board_name=form.board_name.data
    print 'board_id:%s board_name:%s' %(board_id,board_name)
    if form.validate():
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('/delete_board/',methods=['POST'])
@login_required
def delete_board():
    board_id=request.form.get('board_id')
    if not board_id:
        return xtjson.json_params_error(message=u'必须指定版块ID')
    else:
        board = BoardModel.query.filter_by(id=board_id).first()
        if not board:
            return xtjson.json_params_error(message=u'该板块不存在')
        else:
            db.session.delete(board)
            db.session.commit()
            return xtjson.json_result()

@bp.route('/front_users/',methods=['GET'])
@login_required
def cms_front_users():
    front_users=FrontUser.query
    sort=request.args.get('sort',type=int)

    if not sort or sort==1:
        front_users=front_users.order_by(FrontUser.join_time.desc())
    elif sort==2:
        front_users=db.session.query(FrontUser). \
            outerjoin(PostModel).group_by(FrontUser.id).\
            order_by(db.func.count(PostModel.id).desc(),FrontUser.join_time.desc())
    else:
        front_users=db.session.query(FrontUser).outerjoin(CommentModel).\
            group_by(FrontUser.id).order_by(db.func.count(CommentModel.id))



    context=dict(front_users=front_users,sort=sort)
    return render_template('cms/cms_front_users.html',**context)

@bp.route('/edit_frontuser/',methods=['GET','POST'])
@login_required
def cms_edit_frontuser():
    if request.method=='GET':
        user_id = request.args.get('user_id')
        if not user_id:
            abort(404)
        else:
            front_user=FrontUser.query.filter_by(id=user_id).first()
            if not front_user:
                abort(404)
            else:
                context=dict(front_user=front_user)
                return render_template('cms/cms_edit_frontuser.html',**context)
    else:
        form=CMSBlackListF(request.form)
        if form.validate():
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())



# ---------------------钩子函数-------------------------
@bp.before_request
def add_session_to_g():
    cms_user_id=session.get(CMS_USER_ID)

    if cms_user_id:
        cms_user=CMS_User.query.filter_by(id=cms_user_id).first()
        if cms_user:
            g.cms_user=cms_user

@bp.context_processor
def add_g_to_template():
    if hasattr(g,'cms_user'):
        return dict(cms_user=g.cms_user)
    else:
        return {}

# -----------------测试函数-------------------------------