from app import db, ma


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    population = db.Column(db.Integer)
    timezone = db.Column(db.String(200))
    latitude = db.Column(db.String(200))
    longitude = db.Column(db.String(200))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country= db.relationship("Country", backref=db.backref("states", cascade="all, delete-orphan"))
    
    
from models.city import CityNameSchema
class StateSchema(ma.SQLAlchemyAutoSchema):
    cities = ma.Nested(CityNameSchema, many=True)
    class Meta:
        model = State
        load_instance = True
        fields = (
            "id",
            "name",
            "population",
            "timezone",
            "latitude",
            "longitude",
            "country_id",
            "cities"
        )
class StateLoader(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = State
        load_instance = True
        fields = (
            "name",
            "population",
            "timezone",
            "latitude",
            "longitude",
            "country_id"
        )
        
class StateNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = State
        fields = ("name",)
    