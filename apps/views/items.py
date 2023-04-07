import os

from flask import Blueprint, request, render_template, redirect, session
from datetime import datetime

from werkzeug.utils import secure_filename

from model.database import *

user_bp2 = Blueprint('items', __name__)


@user_bp2.route('/home', methods=['GET', 'POST'])
def index():
    ItemsList = db.session.query(Items.user_id, Items, User). \
        filter(Items.user_id == User.id).all()

    ItemsList2 = db.session.query(Items.user_id, Items, User). \
        filter(
        Items.user_id == User.id
    ).order_by(Items.clicknum.desc()).limit(5)

    if request.method == 'POST':
        ItemsList = db.session.query(Items.user_id, Items, User). \
            filter(Items.user_id == User.id,
                   Items.items_title.like("%" + request.form['keyword'] + "%")
                   ).all()
    return render_template(
        "/index.html",
        # Items=Items.query.all()
        Items=ItemsList,
        Items2=ItemsList2
    )


@user_bp2.route("/mycollection", methods=['GET'])
def mycollection():
    if session.get('id') is None:
        return "<script>alert('您未登录，请登录');location.href='/login'</script>"

    likes = db.session.query(Likes, Items).filter(
        Likes.items_userid == session.get('id'),
        Items.id == Likes.items_targetid
    ).all()

    if request.args.get("qx") is not None:
        target = Likes.query.get(request.args.get("qx"))
        db.session.delete(target)
        db.session.commit()

        return "<script>alert('取消成功');location.href='/mycollection'</script>"

    return render_template(
        "/mycollection.html",
        Items=likes
    )


@user_bp2.route("/detail/<string:id>", methods=['GET', 'POST'])
def user_detail(id):
    if session.get('id') is None:
        return "<script>alert('您未登录，请登录');location.href='/login'</script>"

    items = Items.query.get(id)

    user = User.query.get(items.user_id)

    item2 = db.session.query(User, Comment).filter(
        Comment.items_targetid == id, User.id == Comment.items_userid).all()

    like = Likes.query.filter(
        Likes.items_userid == session.get('id')
    ).first()

    clicknum = Items.query.filter(
        Items.id == id
    ).first()

    if (clicknum.clicknum is None):
        clicknum.clicknum = 1;
        db.session.commit()
    else:
        clicknum.clicknum += 1;
        db.session.commit()

    if request.args.get("sc") is not None:
        like = Likes(
            items_time=datetime.now(),
            items_userid=session.get('id'),
            items_targetid=id
        )
        db.session.add(like)
        db.session.commit()
        return "<script>alert('收藏成功');location.href='/detail/" + id + "'</script>"

    if request.method == 'POST':
        comment = Comment(
            items_info=request.form['items_info'],
            items_time=datetime.now(),
            items_userid=session.get('id'),
            items_targetid=id
        )
        db.session.add(comment)
        db.session.commit()
        return "<script>alert('评论成功');location.href='/detail/" + id + "'</script>"

    return render_template(
        "/detail.html",
        items=items,
        user=user,
        id=id,
        item2=item2,
        likes=like
    )


@user_bp2.route("/mypost", methods=['GET'])
def mypost():
    Itemslist = db.session.query(Items, User).filter(
        User.id == session['id'],
        Items.user_id == User.id
    ).all()

    return render_template(
        "/mypost.html",
        Items=Itemslist

    )


@user_bp2.route('/post', methods=['GET', 'POST'])
def post():
    if session.get('id') is None:
        return "<script>alert('您未登录，请登录');location.href='/login'</script>"

    if request.method == 'POST':

        file = request.files['file']
        # filename = ""
        filename = None
        if (file):

            filename = secure_filename(file.filename)

            if filename is not None:
                file.save(os.path.join('./static/upload_files', filename))

        item = Items(
            items_title=request.form['items_title'],
            items_info=request.form['items_info'],
            items_time=datetime.now(),
            user_id=session.get('id'),
            img_url=filename
        )

        db.session.add(item)
        db.session.commit()
        return "<script>alert('发布成功');location.href='/'</script>"

    return render_template(
        "/post.html"
    )
