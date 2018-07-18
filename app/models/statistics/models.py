from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import datetime

from peewee import *

from app import db
from app.utils.auth import token_generator


class BaseModel(Model):
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


MODELS_LIST = [Admins, GameRounds]
