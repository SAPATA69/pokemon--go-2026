import os
from flask import Flask
from pokemon.extensions import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__)

    # ดึงค่า URL จาก environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    @app.register_blueprint(core_bdp, url_prefix='/')

    return app
