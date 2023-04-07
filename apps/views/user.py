import os
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, session
from werkzeug.utils import secure_filename

from model.database import *

user_bp = Blueprint('user2', __name__)



@user_bp.route("/company/jllist/<string:items_id>", methods=['GET', 'POST'])
def jllist(items_id):
    # ItemsList = db.session.query(Post). \
    #     filter(Post.items_id == items_id).all()
    ItemsList = db.session.query(Post,User). \
        filter(Post.items_id == items_id,
               User.id==Post.user_id
               ).all()

    if (request.args.get("ms") is not None):
        p = db.session.query(Post).filter(Post.id == request.args.get("ms")).first()
        p.items_status = 1;
        # 0=待审核
        # 1=面试
        # 2=拒绝

        # company = Company.query.get(request.args.get("delete"))
        # db.session.delete(company)
        db.session.commit()
        return "<script>alert('操作成功');location.href='/company/jllist/"+items_id+"'</script>"

    return render_template(
        "/company/jllist.html",
        # items = Items.query.all()
        items=ItemsList,
        company=Company.query.filter(Company.id == session['company_id']).first()
        ,pagenum=items_id
    )


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        user = User.query.filter(User.account == request.form['account'],
                                 User.pwd == request.form['pwd']).first()

        if user:
            session['user_account'] = user.nickname
            session['id'] = user.id
            return "<script>alert('登录成功');location.href='/home'</script>"
        else:
            return "<script>alert('登录失败');location.href='/login'</script>"
    return render_template("/login.html")


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if (
                request.form['realname'] == '' or
                request.form['idcard'] == '' or
                request.form['nickname'] == '' or
                request.form['phone'] == '' or
                request.form['address'] == '' or
                request.form['account'] == ''
        ):
            return "<script>alert('必须填写全部内容');location.href='/company/register'</script>";

        user = User(
            realname=request.form['realname'],
            idcard=request.form['idcard'],
            nickname=request.form['nickname'],
            phone=request.form['phone'],
            address=request.form['address'],
            account=request.form['account'],
            pwd=request.form['pwd'],
            #jl_url=None
        )
        db.session.add(user)
        db.session.commit()

        return "<script>alert('注册成功');location.href='/login'</script>";

    return render_template("/register.html")


@user_bp.route('/myinfo', methods=['GET', 'POST'])
def my():
    if request.method == 'POST':

        # file = request.files['file']
        # filename = secure_filename(file.filename)
        # if filename is not None:
        # file.save(os.path.join('./static/upload_files', filename))

        user = User.query.filter(User.id == session['id']).first()
        user.realname = request.form['realname']
        user.idcard = request.form['idcard']
        user.nickname = request.form['nickname']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.account = request.form['account']
        user.pwd = request.form['pwd']
        # if filename is not None:
        #user.fj = filename
        # db.session.query.update(user)
        db.session.commit()

        return "<script>alert('修改成功');location.href='/myinfo'</script>";
    user = User.query.filter(User.id == session['id']).first()

    return render_template(
        "/myinfo.html"
        , user=user
    )
