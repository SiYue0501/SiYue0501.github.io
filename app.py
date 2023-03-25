from flask import *
from flask_bootstrap5 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
