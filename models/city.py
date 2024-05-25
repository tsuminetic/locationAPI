from app import db, ma

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    latitude = db.Column(db.String(200))
    longitude = db.Column(db.String(200))
    postal_code=db.Column(db.Integer)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country= db.relationship("Country", backref=db.backref("cities", cascade="all, delete-orphan"))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state= db.relationship("State", backref=db.backref("cities", cascade="all, delete-orphan"))
    
    
class CitySchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = City
        load_instance = True
        fields = (
            "id",
            "name",
            "postal_code",
            "latitude",
            "longitude",
            "country_id",
            "state_id"
        )
        
class CityLoader(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = City
        load_instance = True
        fields = (
            "name",
            "postal_code",
            "latitude",
            "longitude",
            "state_id"
        )
        
        
class CityNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = City
        fields = ("name",)
    