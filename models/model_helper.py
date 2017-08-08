# coding:utf-8
from exts import db
from models.common_models import PostModel,BoardModel,\
    HighlightModel,PostStarModel,CommentModel
from utils.xtredis import BBS_Redis

class PostModelHelper(object):
    class PostModel(object):
        CREATE_TIME=1
        HIGHLIGHT=2
        STAR_COUNT=3
        COMMENT_COUNT=4

    class Delete_Filter(object):
        SHOW_NOT_DELETE=1
        SHOW_ALL=2
        SHOW_ONLY_DELETE=3

    @classmethod
    def post_list(cls,page,sort,board_id,all=1):
        posts = PostModel.query
        boards = BoardModel.query



        # 功能排序
        if not sort or sort == cls.PostModel.CREATE_TIME:
            posts = posts.order_by(PostModel.create_time.desc())
        elif sort == cls.PostModel.HIGHLIGHT:
            posts = db.session.query(PostModel).outerjoin(HighlightModel). \
                group_by(PostModel.id).order_by(HighlightModel. \
                                                create_time.desc(), PostModel.create_time.desc())
        elif sort == cls.PostModel.STAR_COUNT:
            posts = db.session.query(PostModel).outerjoin(PostStarModel). \
                group_by(PostModel.id).order_by(db.func.count(PostStarModel.id).desc(),
                                                PostModel.create_time.desc())
        else:
            posts = db.session.query(PostModel).outerjoin(CommentModel). \
                group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(),
                                                PostModel.create_time.desc())

        # 版块过滤
        if board_id == 0:
            pass
        else:
            posts = posts.filter(PostModel.board_id == board_id)

        if all == cls.Delete_Filter.SHOW_NOT_DELETE:
            posts = posts.filter(PostModel.is_removed == False)
        elif all == cls.Delete_Filter.SHOW_ALL:
            pass
        else:
            posts = posts.filter(PostModel.is_removed == True)

        total_page, pages, start, end = cls.pagination(page=page, total_num=posts.count())
        context = dict(current_page=page, total_page=total_page,
                       pages=pages, posts=posts.slice(start, end),
                       boards=boards, sort=sort, board_id=board_id, all=all)
        return context


    @classmethod
    def post_list_cache(cls, page, sort, board_id, all=1):


        posts=BBS_Redis.post.models(0,50)

        boards=BoardModel.query.all()

        # 功能排序
        if not sort or sort == cls.PostModel.CREATE_TIME:
            posts =sorted(posts,key=lambda post:post.get('create_time'),reverse=True)
            print len(posts)


        elif sort == cls.PostModel.HIGHLIGHT:
            posts = sorted(posts,key=lambda post:(post.get('highlight_id'),post.get('create_time')),reverse=True)


        elif sort == cls.PostModel.STAR_COUNT:
            posts =sorted(posts,key=lambda post:(post.get('star_count'),post.get('create_time')),reverse=True )


        else:
            posts = sorted(posts,key=lambda post:(post.get('comment_count'),post.get('create_time')),reverse=True)

        # 版块过滤
        if board_id == 0:
            pass
        else:
            posts = filter(lambda post:post.get('board_id')==board_id,posts)


        if all == cls.Delete_Filter.SHOW_NOT_DELETE:
            posts = filter(lambda post:post.get('is_removed')==False,posts)
        elif all == cls.Delete_Filter.SHOW_ALL:
            pass
        else:
            posts = filter(lambda post:not post.get('is_removed')==True,posts)



        total_page, pages, start, end = cls.pagination(page=page, total_num=len(posts))


        posts=posts[start:end]


        if page>5:
            context=cls.post_list(page,sort,board_id)
            context.update(total_board_count = BBS_Redis.get('total_board_count'))
        else:

            context = dict(current_page=page,
                           pages=pages, posts=posts,
                           boards=boards, sort=sort, board_id=board_id, all=all,
                           total_page=PostModelHelper.post_list(page, sort, board_id, all).get('total_page'),
                           total_board_count=BBS_Redis.get('total_board_count')
                           )


        return context


    @classmethod
    def pagination(cls,page, total_num, single_num=10, show_pages=5):
        total_page = total_num // single_num
        if total_num % single_num:
            total_page += 1
        start = (page - 1) * single_num
        end = page * single_num

        tmp_page = page - 1
        pages_li = []
        while tmp_page >= 1:
            if tmp_page % show_pages:
                pages_li.append(tmp_page)
                tmp_page -= 1
            else:
                break

        tmp_page = page
        while tmp_page <= total_page:
            pages_li.append(tmp_page)
            if tmp_page % show_pages:
                tmp_page += 1
            else:
                break
        pages_li.sort()

        return (total_page, pages_li, start, end)