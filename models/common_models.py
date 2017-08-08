# coding:utf-8
from exts import db
from models.base_models import BaseModel
from datetime import datetime
from models.front_models import FrontUser
from models.cms_models import CMS_User

class BoardModel(db.Model,BaseModel):
    __tablename__='board'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('cms_user.id'))

    author=db.relationship('CMS_User',backref='boards')

    def to_dict(self):
        model_dict=super(BoardModel, self).to_dict()
        model_dict.update(post_count=self.posts.count() if self.posts else 0)
        return model_dict

class HighlightModel(db.Model,BaseModel):
    __tablename__='highlight'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))


class PostModel(db.Model,BaseModel):
    __tablename__='post'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    update_time=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    read_count=db.Column(db.Integer,default=0)
    is_removed=db.Column(db.Boolean,default=False)

    board_id=db.Column(db.Integer,db.ForeignKey('board.id'))
    author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))
    highlight_id=db.Column(db.Integer,db.ForeignKey('highlight.id'))

    board=db.relationship('BoardModel',backref=db.backref('posts',lazy='dynamic'))
    author=db.relationship('FrontUser',backref='posts')
    highlight=db.relationship('HighlightModel',backref='post')

    def to_dict(self):
        model_dict=super(PostModel, self).to_dict()
        model_dict.update(
            board=self.board.to_dict(),
            author=self.author.to_dict(),
            star_count=len(self.stars) if self.stars else 0,
            comment_count=len(self.comments) if self.comments else 0
                           )


        return model_dict

class PostStarModel(db.Model,BaseModel):
    __tablename__='post_star'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))

    author=db.relationship('FrontUser',backref='stars')
    post=db.relationship('PostModel',backref='stars')

class CommentModel(db.Model,BaseModel):
    __tablename__='comment'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    is_removed=db.Column(db.Boolean,default=False)

    author_id=db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    origin_comment_id=db.Column(db.Integer,db.ForeignKey('comment.id'))

    author=db.relationship('FrontUser',backref='comments')
    post=db.relationship('PostModel',backref='comments')
    origin_comment=db.relationship('CommentModel',backref='replys',remote_side=[id])

    def to_dict(self):
        model_dict=super(CommentModel,self).to_dict()
        model_dict.update(author=self.author.to_dict(),
                          post=self.post.to_dict(),
                          origin_comment=self.origin_comment.to_dict() if self.origin_comment else False)
        return model_dict