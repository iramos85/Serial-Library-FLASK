
from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('killer_profiles.sqlite')

class User(UserMixin, Model):
    name=CharField(unique=False)
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE

class Killer(Model):
    # Columns
    name = CharField()
    active = CharField()
    summary = CharField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    # Creating table when we're initializing
    DATABASE.create_tables([User, Killer], safe=True)
    print("TABLES Created", Database)
    DATABASE.close()

