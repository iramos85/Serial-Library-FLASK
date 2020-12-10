import models
from numpy import genfromtxt
from time import time
from datetime import datetime
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import pandas
import csv
import random


killer = Blueprint('killers', 'killer')

# current directory is this '/api/v1/killers'
@killer.route('/', methods=["GET"])
def get_all_killers():
    killers = models.Killer.select()
    killer_dicts = [model_to_dict(killer) for killer in killers]
    try:
        print(killer_dicts)
        return jsonify(data=killer_dicts, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@killer.route('/<id>', methods=["GET"])
def get_one_killer(id):
    killer = models.Killer.get_by_id(id)
    return jsonify(data=model_to_dict(killer), status={"code": 200, "message": "Success"})

@killer.route('/random', methods=["GET"])
def get_random_killer():
    random_profile = random.randint(0,650)
    killer = models.Killer.get_by_id(random_profile)
    
    return jsonify(data=model_to_dict(killer), status={"code": 200, "message": "Success"})

##DO NOT USE THIS ROUTE. THIS WAS FOR THE INITIAL CREATION OF THE DATABASE##
@killer.route('/seed', methods=["GET"])
def make_database():
    df = pandas.read_csv('/Users/ianramos85/GA/Capstone/Serial_Library/Backend-FLASK/Data/killer_profiles.csv')
    for row in df.iterrows():
        models.Killer.create(
            name=row[1].Name,
            active=row[1].Active,
            summary=row[1].Summary)

    return jsonify(data={}, status={"code": 200, "message": "Success"})

