from flask import Blueprint, request, render_template, redirect, session
from model.database import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    session.clear()
    if request.method == "POST":
        admin = Admin.query.filter(Admin.loginname == request.form['username'],
                                   Admin.loginpwd == request.form['password']).first()

        if admin:
            session['admin'] = admin.loginname
            session['admin_id'] = admin.id
            return "<script>alert('登录成功');location.href='/admin'</script>"
        else:
            return "<script>alert('登录失败');location.href='/admin/login'</script>"

    return render_template(
        "/admin/login.html"
    )


@admin_bp.route('/admin/userlist', methods=['GET', 'POST'])
def admin_userlist():
    if session.get('admin') is None:
        return "<script>alert('请登录管理员账号');location.href='/admin/login'</script>"

    if (request.args.get("delete") is not None):
        user = User.query.get(request.args.get("delete"))
        db.session.delete(user)
        db.session.commit()
        return "<script>alert('删除成功');location.href='/admin/userlist'</script>"

    ItemsList = User.query.all()

    if request.method == 'POST':
        ItemsList = User.query \
            .filter(User.realname.like("%" + request.form['keyword'] + "%")) \
            .all()
    # .filter(Company.company_name.like("%" + request.form['keyword'] + "%"))\
    return render_template(
        "/admin/userlist.html",
        Items=ItemsList,
    )


@admin_bp.route('/admin/comment', methods=['GET', 'POST'])
def admin_comlist():
    if session.get('admin') is None:
        return "<script>alert('请登录管理员账号');location.href='/admin/login'</script>"

    if (request.args.get("delete") is not None):
        target = Comment.query.get(request.args.get("delete"))
        db.session.delete(target)
        db.session.commit()
        return "<script>alert('删除成功');location.href='/admin/comment'</script>"

    ItemsList = db.session.query(Items, Comment, User).filter(
        Items.id == Comment.items_targetid,
        Comment.items_userid == User.id
    ).all()

    if request.method == 'POST':
        # ItemsList = User.query \
        #     .filter(User.realname.like("%" + request.form['keyword'] + "%")) \
        #     .all()
        ItemsList = db.session.query(Items, Comment, User).filter(
            Items.id == Comment.items_targetid,
            Comment.items_userid == User.id,

        ).all()

    return render_template(
        "/admin/comlist.html",
        Items=ItemsList,
    )


@admin_bp.route('/admin/index', methods=['GET', 'POST'])
@admin_bp.route('/admin', methods=['GET', 'POST'])
@admin_bp.route('/admin/blogs', methods=['GET', 'POST'])
def admin_blogs():
    if session.get('admin') is None:
        return "<script>alert('请登录管理员账号');location.href='/admin/login'</script>"

    if (request.args.get("delete") is not None):
        item = Items.query.get(request.args.get("delete"))
        db.session.delete(item)
        db.session.commit()
        return "<script>alert('删除成功');location.href='/admin/userlist'</script>"

    ItemsList = Items.query.all()

    if request.method == 'POST':
        ItemsList = Items.query \
            .filter(Items.items_title.like("%" + request.form['keyword'] + "%")) \
            .all()
    # .filter(Company.company_name.like("%" + request.form['keyword'] + "%"))\
    return render_template(
        "/admin/zpgl.html",
        Items=ItemsList,
    )


@admin_bp.route('/admin/indexedit/<int:id>', methods=['GET', 'POST'])
def admin_indexedit(id):
    items = Items.query.filter(Items.id == id).first()

    if request.method == 'POST':
        items.phone = request.form['']
        items.loginname = request.form['']
        items.loginpwd = request.form['']
        db.session.commit()
        return "<script>alert('修改成功');location.href='/admin/index'</script>"

    return render_template(
        "/admin/indexedit.html",
        phone=items.company_phone,
        loginname=items.company_loginname,
        loginpwd=items.company_loginpwd
    )
