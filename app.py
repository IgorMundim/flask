
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from routes import user, task, category
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    # database setup.
    basedir = os.path.dirname(__file__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'todo.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = "a3dac879b642971c8f36a00d2372ecb5f0f10ab747908b95b98bdde24709dc65"
    Bootstrap(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(task.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(category.bp)
    
    return app

    # Create bank from terminal 
    # python 3
    # >>> from app import db
    # >>> from extensions import db
    # >>> from app import create_app
    # >>> from models import *
    # >>> db.create_all(app=create_app())
