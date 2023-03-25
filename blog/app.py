# 导入flask项目
from flask import *

# 实例化flask
app = Flask(__name__)


@app.route('/')  #
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login')
def login():
    return "你好"


@app.route('/register')
def register():
    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run()
