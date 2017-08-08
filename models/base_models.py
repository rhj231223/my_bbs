# coding:utf-8
from exts import db
from datetime import datetime
import json

class BaseModel(object):
    def to_dict(self):
        columns=self.__table__.columns
        col_dict={}
        for column in columns:
            value=getattr(self,column.name)
            if isinstance(value,datetime):
                value=value.strftime('%Y:%m:%d %H:%M:%S')
            col_dict[column.name]=value
        return col_dict

    def to_json(self):
        return json.dumps(self.to_dict())