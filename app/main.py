from flask import Flask, session
from controller.routes import init_app 
from views.jinja_filters import datetimeformat
import os

app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
app.secret_key = os.getenv('SECRET_KEY')
app.jinja_env.filters['dateFormat'] = datetimeformat
init_app(app)

if __name__ == '__main__':
    app.run(debug=True)