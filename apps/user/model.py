# ORM 对象关系映射  类 ----》表
# 类对象----〉数据库中的表
from datetime import datetime

from ext import db


class User(db.Model):
    # db.Column(类型，约束) 映射表中的列
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(30))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    # 增加字段 view和template使用
    articles = db.relationship('Article', backref='user')

    def __str__(self):
        return self.username
