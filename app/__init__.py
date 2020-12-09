from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pretty import Prettify

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'profile.login'
login.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap()
moment = Moment()
prettify = Prettify()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    prettify.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.ncaa import bp as ncaa_bp
    app.register_blueprint(ncaa_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    app.jinja_env.globals.update({
        'Comment': models.Comment,
        'User': models.User,
        'Team': models.Team,
        'Conference': models.Conference
    })

    return app


from app import models
