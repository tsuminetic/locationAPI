from app import db, ma


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    population = db.Column(db.Integer)
    timezone = db.Column(db.String(200))
    latitude = db.Column(db.String(200))
    longitude = db.Column(db.String(200))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    
class StateSchema(ma.SQLAlchemyAutoSchema):
    
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
            "country_name"
        )
    