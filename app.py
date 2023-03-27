from flask import *
from flask_bootstrap5 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["user"]
        pwd = request.form["password"]
        if name == "11" and pwd == "11":
            return render_template("shouye.html")
        else:
            return render_template("login.html", msg="密码错误")
    else:
        return render_template("404.html")


if __name__ == '__main__':
    app.run()
