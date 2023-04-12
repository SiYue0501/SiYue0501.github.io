from flask import *
from flask_bootstrap5 import Bootstrap
from model.database import db
from model.config import *
from apps.views.user import user_bp
from apps.views.items import user_bp2
from apps.views.admin import admin_bp
import apps.views.admin
import json
import pymysql

app = Flask(__name__)
app.secret_key = 'xxxxxxx'
app.register_blueprint(user_bp)
app.register_blueprint(user_bp2)
app.register_blueprint(admin_bp)

bootstrap = Bootstrap(app)

app.config.from_object(DefaultConfig)
app.secret_key = 'xxxxxxx'
db.init_app(app)


@app.route('/')  # 当点击提交时会跳转到login的路由地址
def hello_world():  # put application's code here
    return render_template("start.html")


if __name__ == '__main__':
    app.run()
