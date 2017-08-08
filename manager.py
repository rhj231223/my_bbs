# coding:utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from exts import app,db
from models.cms_models import CMS_User,CMS_Role,cms_user_role,CMS_Permission
from models import cms_models,front_models,common_models

manager=Manager(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-n','--name',dest='name')
@manager.option('-d','--desc',dest='desc')
@manager.option('-p','--permission',dest='permission')
def add_cms_role(name,desc,permission):
    name=name.decode('gbk').encode('utf-8')
    desc=desc.decode('gbk').encode('utf-8')
    permission=permission.decode('gbk').encode('utf-8')

    db_name=CMS_Role.query.filter_by(name=name).first()
    if db_name:
        print u'this role is exist'

    else:
        role=CMS_Role(name=name,desc=desc,permission=permission)
        db.session.add(role)
        db.session.commit()
        print u'role append success'

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
@manager.option('-r','--roles',dest='roles')
def add_cms_user(username,password,email,roles):
    username=username.decode('gbk').encode('utf-8')
    email=email.decode('gbk').encode('utf-8')
    password=password.decode('gbk').encode('utf-8')
    roles=roles.decode('gbk').encode('utf-8')

    db_email=CMS_User.query.filter_by(email=email).first()
    if db_email:
        print u'this email is exist can regist'
    else:
        user=CMS_User(username=username,password=password,email=email)
        role_model=CMS_Role.query.filter_by(name=roles).first()
        user.roles.append(role_model)
        db.session.add(user)
        db.session.commit()
        print u'regist success'






if __name__=='__main__':
    manager.run()

