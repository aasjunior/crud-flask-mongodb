from flask import Flask
from controller import routes 
from views.jinja_filters import datetimeformat

app = Flask(__name__, template_folder='views/templates')
app.jinja_env.filters['dateFormat'] = datetimeformat
routes.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)