
from flask import Flask, jsonify, g, request, redirect, url_for

from flask_cors import CORS
from resources.killers import killer # adding this line
from resources.users import user
import models


from flask_login import LoginManager

DEBUG = True
PORT = 8000

app = Flask(__name__)


# configuring the LoginManager according to this
# https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# we need to do several things

#1. we need to set up a secret/key for sessions
# as demonstated here: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
app.secret_key = "List of the Damned"

#2. instantiate the LoginManager to actually get a login_manager
login_manager = LoginManager()

#3. actually connect the app with the login manager
login_manager.init_app(app) #set up sessions on the app

@login_manager.user_loader
def load_user(user_id):
    try:
        print('loading the following user')
        user = models.User.get_by_id(user_id) #IMPORTANT CHANGE
                                            # USE get_by_id

        return user

    except models.DoesNotExist:
        return None



CORS(killer, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
CORS(user, origins=['http://localhost:3000'], supports_credentials=True) # adding this line

# Similiar to this in Javascript: app.use('/api/v1/killers', controller)
app.register_blueprint(killer, url_prefix='/api/v1/killers') # adding this line
app.register_blueprint(user, url_prefix='/api/v1/users')



@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

# This notation is known as a decorator, it's a higher order function
# that imports the function that it's decorating and adds logic to it.
@app.route('/')
def index():
	return "Hello"

@app.route('/profile/<username>')
def profile(username):

    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username = session['username'])

    if user is None:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html')


# When we run this file, everything below this is our executable
# logic
if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)