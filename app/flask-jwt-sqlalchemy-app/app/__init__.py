from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import models here, after db.init_app(app)
        from . import models, routes, auth, project_routes
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(project_routes.project_bp)
        app.register_blueprint(routes.routes_bp)

        db.create_all()

    return app