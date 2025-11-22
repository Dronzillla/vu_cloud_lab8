from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade


db = SQLAlchemy()


def create_app(config_class="config.config.DevelopmentConfig"):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Set up db
    db.init_app(app)

    # Import and register API-only blueprint (we're converting to an API service)
    # Do not register UI blueprints to disable frontend routes.
    from blueprintapp.blueprints.api.routes import alerts

    # Register the alerts API at /api
    app.register_blueprint(alerts, url_prefix="/api")

    migrate = Migrate(app, db)

    # Locally run 'docker-compose up-d' command to run postgre from docker file
    # docker-compose down -v
    # docker-compose ps
    # docker-compose up -d

    # To create db go to the folder /blueprintapp where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    return app
