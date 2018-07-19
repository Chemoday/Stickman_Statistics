from flask import Flask
from flask_peewee.db import Proxy
from flask_bootstrap import Bootstrap

from app.config import config_select

db = Proxy()
bootstrap = Bootstrap()


def create_app(config_name="None"):
    app = Flask(__name__)


    #default config = production
    if config_name==None:
        config_name = 'default'


    app.config.from_object(config_select[config_name])
    db.initialize(config_select[config_name].DATABASE) #initialize a real db via proxy
    bootstrap.init_app(app)

    #register blueprints
    from app.blueprint.main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.blueprint.auth_http import auth_api
    app.register_blueprint(auth_api)

    from app.blueprint.statistics import statistics
    app.register_blueprint(statistics)

    from app.blueprint.analytics import analytics
    app.register_blueprint(analytics)


    return app