from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import DevConfig
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes import blueprint as routes_blueprint
    app.register_blueprint(routes_blueprint)

    from app.views import blueprint as views_blueprint
    app.register_blueprint(views_blueprint)

    return app


from app import models
