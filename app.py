from flask import *
from flask_bootstrap5 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')  # 当点击提交时会跳转到login的路由地址
def hello_world():  # put application's code here
    return render_template("index_tem.html")


@app.route("/denglu", methods=["POST", "GET"])
def denglu():
    return render_template("login.html")


@app.route("/zhuce", methods=["POST", "GET"])
def zhuce():
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["user"]
        pwd = request.form["password"]
        if name == "11" and pwd == "11":
            return render_template("shouye.html")
        else:
            return render_template("login.html", msg="账号或密码有误！")
    else:
        return render_template("404.html")


if __name__ == '__main__':
    app.run()
