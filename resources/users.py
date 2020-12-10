import models
from flask import Blueprint, request, jsonify, request, redirect, url_for
from functools import wraps
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

user = Blueprint('users','user')

@user.route('/', methods=['GET'])
def test_user_resource():
    users = models.User.select()
    user_dicts = [ model_to_dict(user) for user in users ]

    for user_dict in user_dicts:
        user_dict.pop('password')

        print(user_dicts)

        return jsonify(user_dicts), 200

@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    print(payload)
    payload['name'] = payload['name'].lower()
    # since emails are case insensitive in the world
    payload['email'] = payload['email'].lower()
    # we will do the same with username
    payload['username'] = payload['username'].lower()
    # print(payload)
    payload['password'] = payload['password'].lower()

    try:

        models.User.get(models.User.email == payload['email'])
        # this will throw an error ("models.DoesNotExist exception")

        # if so -- we don't want to create the user
        # response: "user with that email already exists"
        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401

    except models.DoesNotExist: 
        # the user does not exist
        # scramble the password with bcrypt
        pw_hash = generate_password_hash(payload['password'])

        # create them
        created_user = models.User.create(
            name=payload['name'],
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )
        # respond with new object and success message
        print(created_user)
        created_user_dict = model_to_dict(created_user)
        print(created_user_dict)

        login_user(created_user)

        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201

@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['password'] = payload['password'].lower()
    payload['username'] = payload['username'].lower()

    try:
        user = models.User.get(models.User.username == payload['username'])

        user_dict = model_to_dict(user)

        password_is_good = check_password_hash(user_dict['password'], payload['password'])

        if(password_is_good):
            # LOG THE USER IN!!! using flask-login
            login_user(user) # in express we did this manually by setting stuff in the session
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['username']}",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="username or password is incorrect", #let's be vague
                status=401
            ), 401


    except models.DoesNotExist:
        return jsonify(
            data={},
            message="username or password is incorrect", #let's be vague
            status=401
        ), 401



@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message="successful logout",
        status=200
    ), 200

# @user.route('/<username>', method=['GET'])
# def user():
#     print('this is the user profile page')
# #     user = User.query.filter_by(username=username).first_or_404()
# #     readingList = [
# #         {'Killer 1', 'Test post #1'},
# #         {'Killer 2', 'Test post #2'}
# #     ]
#     # return jsonify(
#     #     data={},
#     #     message='successfully hit profile page',
#     #     status=200
#     # )



