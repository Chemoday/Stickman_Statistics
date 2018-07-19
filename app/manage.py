
#Define Python project in PYTHONPATH
import sys
from os.path import dirname, abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.append(PROJECT_DIR)

#Initial project
from app import create_app
from flask_script import Manager



manager = Manager(create_app)



@manager.command
def generate_db_stat_tables():
    from app import db

    from config import DevelopmentConfig
    db.initialize(DevelopmentConfig.DATABASE)
    from models.statistics.models import MODELS_LIST
    db.create_tables(MODELS_LIST, safe=True)
    print("Db tables created")



manager.add_option('-c', '--config', dest='config_name', required=False)



if __name__ == '__main__':
    manager.run()

