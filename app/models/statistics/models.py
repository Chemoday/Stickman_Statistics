from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import datetime

from peewee import *

from app import db
from app.utils.auth import token_generator


class BaseModel(Model):
    CASH_SIZE = 15
    #CASH_TYPE Used to store models to bulk insert after
    #reduced load on database
    CASH_TYPE = {
        'gameRounds': [],
        'tutorialFlow': [],
        'settingsJoystick': []
    }



    @classmethod
    def insert_bulk_data(cls, data_to_insert):
        with db.atomic():
            cls.insert_many(data_to_insert).execute()


    @classmethod
    def check_cache_condition(cls, cache_type, data):
        if len(cls.CASH_TYPE[cache_type]) >= cls.CASH_SIZE:
            try:
                cls.insert_bulk_data(data_to_insert=cls.CASH_TYPE[cache_type])
                cls.CASH_TYPE[cache_type].clear() #delete all data from CASH of cache_type
                print('Pushed to db')
            except Exception as e:
                print(e)
        else:
            cls.CASH_TYPE[cache_type].append(data)

    class Meta:
        database = db
        schema = 'stat'

class Admins(BaseModel):
    last_login_dt = DateTimeField(null=True)
    moderator = BooleanField(constraints=[SQL("DEFAULT false")])
    password = CharField(null=True)
    token = CharField(null=True)
    token_created_dt = DateTimeField(null=True)
    username = CharField(null=True)
    id = PrimaryKeyField()

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def password_hash(self):
        raise AttributeError or('password is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        return token_generator.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        try:
            data = token_generator.loads(token)
        except SignatureExpired:
            return None, SignatureExpired  # valid token, but expired
        except BadSignature:
            return None, None  # invalid token
        admin = Admins.get(Admins.id == data['id'])
        return admin, None

    class Meta:
        table_name = 'admins'

class GameRounds(BaseModel):
    #TODO ask Kostja about map format
    mode = CharField(index=True, max_length=20)
    type = CharField(index=True, max_length=20)
    map = CharField(index=True, max_length=20)
    total_players = IntegerField()
    total_kills = IntegerField()
    total_deaths = IntegerField()
    most_kills = IntegerField()
    most_deaths = IntegerField()
    created_dt = DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'game_rounds'


class TutorialFlow(BaseModel):
    phase = CharField(index=True, max_length=25)
    completion_time = IntegerField(default=0)
    deaths = IntegerField(default=0)
    grenade_used = BooleanField(default=False)
    weapon_changed = BooleanField(default=False)
    crouch_used = BooleanField(default=False)


    class Meta:
        table_name = 'tutorial_flow'

class SettingsJoystick(BaseModel):
    user_id = IntegerField(unique=True)
    controls_type = CharField(index=True)
    changed = BooleanField(default=0)

    class Meta:
        table_name = 'settings_joystick'


MODELS_LIST = [Admins, GameRounds, TutorialFlow, SettingsJoystick]
