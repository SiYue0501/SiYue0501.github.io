from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 数据模型
class User(db.Model):
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    nickname = db.Column(db.String(255))
    account = db.Column(db.String(255))
    pwd = db.Column(db.String(255))
    realname = db.Column(db.String(255))
    idcard = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __init__(self, nickname, account, pwd, realname, idcard, address, phone):
        self.nickname = nickname
        self.account = account
        self.pwd = pwd
        self.realname = realname
        self.idcard = idcard
        self.address = address
        self.phone = phone
        # self.status = 0


class Comment(db.Model):
    __tablename__ = "tb_comment"
    id = db.Column(db.Integer, primary_key=True)
    items_info = db.Column(db.Text)
    items_userid = db.Column(db.Integer)
    items_targetid = db.Column(db.Integer)
    items_time = db.Column(db.Integer)

    def __init__(self, items_info, items_time, items_userid, items_targetid):
        self.items_info = items_info
        self.items_time = items_time
        self.items_userid = items_userid
        self.items_targetid = items_targetid


class Likes(db.Model):
    __tablename__ = "tb_likes"
    id = db.Column(db.Integer, primary_key=True)
    items_userid = db.Column(db.Integer)
    items_targetid = db.Column(db.Integer)
    items_time = db.Column(db.Integer)

    def __init__(self, items_time, items_userid, items_targetid):
        self.items_time = items_time
        self.items_userid = items_userid
        self.items_targetid = items_targetid


class Items(db.Model):
    __tablename__ = "tb_items"
    id = db.Column(db.Integer, primary_key=True)
    items_title = db.Column(db.String(255))
    items_info = db.Column(db.Text)
    items_time = db.Column(db.DateTime)
    img_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    clicknum = db.Column(db.Integer)

    def __init__(self, items_title,
                 items_info,
                 items_time,
                 user_id, img_url):
        self.items_title = items_title
        self.items_info = items_info
        self.items_time = items_time
        self.user_id = user_id
        self.img_url = img_url


class Admin(db.Model):
    __tablename__ = "tb_admin"
    id = db.Column(db.Integer, primary_key=True)
    loginname = db.Column(db.String(255))
    loginpwd = db.Column(db.String(255))


class Post(db.Model):
    __tablename__ = "tb_post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_note = db.Column(db.String(255))
    post_time = db.Column(db.DateTime)
    items_id = db.Column(db.Integer)
    items_status = db.Column(db.Integer)

    def __init__(self, user_id, post_note, post_time, items_id):
        self.user_id = user_id
        self.post_note = post_note
        self.post_time = post_time
        self.items_id = items_id
        self.items_status = 0

# def test():
#     return jsonify()
