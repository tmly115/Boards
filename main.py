from flask import Flask
from user_managment import user_managment
from main_app import main_app

import app_config

app = Flask(__name__)

app.secret_key = 'Hdsnl123KKraoj2io4'

app.register_blueprint(user_managment)
app.register_blueprint(main_app)

if __name__ == '__main__':
    app.run(debug = True)
