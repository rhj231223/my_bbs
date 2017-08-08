# coding:utf-8
from flask import Blueprint,render_template,\
    url_for,request,session,abort,jsonify,g
from decorators.front_decorators import login_required
from models.front_models import FrontUser
from models.common_models import BoardModel,PostModel,\
    HighlightModel,PostStarModel,CommentModel
from constants import ACCESS_KEY,SECRET_KEY
from forms.front_forms import FrontAddPostForm,\
    FrontAddCommentForm,FrontPostStarForm
from utils import xtjson
from exts import db
from models.model_helper import PostModelHelper
from utils.xtredis import BBS_Redis
from exts import app
import qiniu,random,threading

bp=Blueprint('post',__name__)



@bp.route('/')
def post_index():
    return list_page(page=1,sort=1,board_id=0)

@bp.route('/list_page/<int:page>/<int:sort>/<int:board_id>/')
def list_page(page,sort,board_id=0,all=1):
    # if page<6:
    context = PostModelHelper.post_list(page, sort, board_id, all)
    # else:
    #     context=PostModelHelper.post_list(page,sort,board_id,all)
    #     context.update(total_board_count=BBS_Redis.get('total_board_count'))

    return render_template('front/front_index.html',**context)

@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    post=filter(lambda post:post.get('id')==post_id,BBS_Redis.post.models())[0]
    if not post:
        post=PostModel.query.filter_by(post_id=post_id).first()
    stars=PostStarModel.query.filter_by(post_id=post_id)
    star_author_ids = [star.author.id for star in stars]
    comments=filter(lambda comment:comment.get('post_id')==post_id,BBS_Redis.comment.models())
    db_comments=CommentModel.query.filter_by(post_id=post_id).all()
    comment_ids=[comment.get('id') for comment in comments]
    diff_comments=filter(lambda db_comment:db_comment.id not in comment_ids,db_comments)

    highlight=HighlightModel.query.filter_by(id=post.get('highlight_id')).first()
    comment_count=len(comments)+len(diff_comments)

    context=dict(post=post,stars=stars,star_author_ids=star_author_ids,
                 comments=comments,diff_comments=diff_comments,
                 comment_count=comment_count,highlight=highlight)
    return render_template('front/front_post_detail.html',**context)


def hello():
    return 'hello'


@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    if request.method=='GET':
        boards=BoardModel.query.all()
        context=dict(boards=boards)
        return render_template('front/front_add_post.html',**context)
    else:
        form=FrontAddPostForm(request.form)
        if form.validate():
            title=form.title.data
            board_id=form.board_id.data
            content=form.content.data

            board=BoardModel.query.filter_by(id=board_id).first()

            post=PostModel(title=title,content=content)
            post.board=board
            post.author=g.front_user
            db.session.add(post)
            post.author.points+=random.randint(8,10)
            db.session.commit()

            BBS_Redis.post.active_flush(post)

            return xtjson.json_result()

        else:
            return xtjson.json_params_error(message=form.get_error())


@bp.route('/add_comment/<int:post_id>/',methods=['GET','POST'])
@login_required
def front_add_comment(post_id):
    if request.method=='GET':
        post = PostModel.query.filter_by(id=post_id).first()
        comment_id = request.args.get('comment_id')
        context = dict(post=post)
        if comment_id:
            comment = CommentModel.query.filter_by(id=comment_id).first()
            context.update(comment=comment)
        return render_template('front/front_add_comment.html',**context)
    else:
        form=FrontAddCommentForm(request.form)
        if form.validate():
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

@bp.route('/post_star/',methods=['POST'])
@login_required
def post_star():
    form=FrontPostStarForm(request.form)
    if form.validate():
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


@bp.route('/qiniu_token_mybbs/')
def qiniu_token():
    q=qiniu.Auth(ACCESS_KEY,SECRET_KEY)

    bucket_name='mybbs'

    token=q.upload_token(bucket_name)
    return jsonify(dict(uptoken=token))

# ---------------------测试函数-------------------------------




@bp.route('/test/')
def test():
    # board=BoardModel.query.first()
    # author=FrontUser.query.first()
    # for i in range(100):
    #     title=u'标题:%s' %i
    #     content=u'内容:%s' %i
    #
    #     post=PostModel(title=title,content=content)
    #     post.board=board
    #     post.author=author
    #     db.session.add(post)
    # db.session.commit()
    # return 'success'

    posts=PostModel.query.filter_by(is_removed=False).order_by(PostModel.create_time.desc()).all()
    boards=BoardModel.query.all()
    comments=CommentModel.query.filter_by(is_removed=False).order_by(CommentModel.create_time.desc()).all()

    if len(posts)>=50:
        for post in posts[:50]:
            BBS_Redis.post.add_model(post)

            count=0
            for comment in comments:
                if post.id ==comment.post.id:
                    BBS_Redis.comment.add_model(comment)
                    count+=1
                    if count==50:
                        count=0
                        continue


    for board in boards:
        BBS_Redis.board.add_model(board)

    BBS_Redis.set('total_board_count',104)
    #
    #
    #
    # post=PostModel.query.get(16)
    # author=FrontUser.query.first()
    # for i in range(50):
    #     content='评论%s！' %i
    #     comment=CommentModel(content=content)
    #     comment.post=post
    #     comment.author=author
    #     db.session.add(comment)
    # db.session.commit()
    return 'success'

@bp.route('/test_2/')
def test_2():
    user=FrontUser(username='rhj231223',password='2312231223',
                   telephone=18221968578)
    db.session.add(user)
    db.session.commit()
    return 'success'



# def flush():
#     BBS_Redis.delete('second_post')
#     BBS_Redis.delete('second_board')
#     BBS_Redis.delete('second_comment')
#     with app.app_context():
#         test()
#
# threading._Timer(300, flush).start()
