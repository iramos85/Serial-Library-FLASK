import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect



if 'ON_HEROKU' in os.environ: # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
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
    summary = TextField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    # Creating table when we're initializing
    DATABASE.create_tables([User, Killer], safe=True)
    print("TABLES Created", Database)
    DATABASE.close()

