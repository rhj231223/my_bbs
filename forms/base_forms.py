# coding:utf-8
from flask_wtf import FlaskForm

class BaseForm(FlaskForm):
    def get_error(self):
        _,value=self.errors.popitem()
        message=value[0]
        return message

        # li=[]
        # for v in self.errors.values():
        #     li.append(v[0])
        #
        # message='<br>'.join(li)
        # return message
