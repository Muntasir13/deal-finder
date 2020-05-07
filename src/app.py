from flask import Flask, render_template
import secrets

from common import config
from common.database import Database
from models.deals.deals import Deals
from models.deals.views import deals_blueprint
from models.users.views import users_blueprint


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = secrets.token_urlsafe()


@app.before_first_request
def database_initialize():
    Database.initialize()


@app.route('/')
def index():
    return render_template('index.html', deals=Deals.featured_deals())


@app.route('/teams')
def teams():
    return render_template('teams.html')


app.register_blueprint(users_blueprint, url_prefix="")
app.register_blueprint(deals_blueprint, url_prefix="")

