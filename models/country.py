from app import db, ma


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    capital = db.Column(db.String(100))
    population = db.Column(db.Integer)
    currency = db.Column(db.String(50))
    official_language = db.Column(db.String(200))
    continent = db.Column(db.String(50))
    iso_code = db.Column(db.String(10), unique=True)
    calling_code = db.Column(db.String(10))
    timezone = db.Column(db.String(200))


class CountrySchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Country
        load_instance = True
        fields = (
            "id",
            "name",
            "capital",
            "population",
            "currency",
            "official_language",
            "continent",
            "iso_code",
            "calling_code",
            "timezone"
        )
