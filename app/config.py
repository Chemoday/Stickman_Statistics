import os
import peewee
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    POSTS_PER_PAGE = 10
    TOKEN_LIFETIME = 600


    #manage stuff
    REGISTRATION_OPEN = True




class DevelopmentConfig(Config):
    DEBUG = True

    host= 'localhost'
    port= 5444
    user= 'postgres'
    password = 'postgres'
    DATABASE = peewee.PostgresqlDatabase('stickman', user=user, password=password,
                                         host=host, port=port, autorollback=False)


class ProductionConfig(Config):
    DEBUG = False

    host= 'localhost'
    port= 5444
    user= 'postgres'
    password = 'postgres'
    DATABASE = peewee.PostgresqlDatabase('stickman', user=user, password=password,
                                         host=host, port=port, autorollback=True)

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE = {
        'name': 'test.db',
        'engine': 'peewee.SqliteDatabase'
    }

    @property
    def database_type(self):
        return peewee.SqliteDatabase('test.db')

config_select = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}