from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

app=Flask(__name__)

app.config['SECRET_KEY']='dasjhghjasbdas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models.country import Country, CountrySchema
from models.state import State, StateSchema
from models.city import City, CitySchema

with app.app_context():
    db.create_all()