from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Option with DB migrations
# from flask_migrate import Migrate, upgrade


db = SQLAlchemy()


def create_app(config_class="config.config.DevelopmentConfig"):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Set up db
    db.init_app(app)

    from blueprintapp.blueprints.api.routes import alerts

    # Register the alerts API at /api
    app.register_blueprint(alerts, url_prefix="/api")

    # Option with database migrations
    # migrate = Migrate(app, db)

    # Locally run 'docker-compose up-d' command to run postgre from docker file
    # docker-compose down -v
    # docker-compose ps
    # docker-compose up -d

    # Option with database migrations
    # To create db go to the folder /blueprintapp where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    # Option without database migrations
    with app.app_context():
        db.create_all()

    return app
