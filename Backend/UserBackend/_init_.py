from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")

    from app.routes.issues import issues as issues_blueprint

    app.register_blueprint(issues_blueprint, url_prefix="/api/issues")

    # Create database tables
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}, 200

    return app
