from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from models.country import Country, CountrySchema,CountryLoader
from werkzeug.exceptions import BadRequest

api = Blueprint('country_api', __name__)

# List all countries
@api.route('', methods=['GET'])
def get_all():
    countries = Country.query.all()
    country_schema = CountrySchema(many=True)
    data = country_schema.dump(countries)
    return jsonify({"data": data, "metadata": {"total": len(countries)}})

# Get a specific country
@api.route('/<int:country_id>', methods=['GET'])
def get_country(country_id):
    country = Country.query.get(country_id)
    if not country:
        raise BadRequest("resource not found")

    country_schema = CountrySchema()
    data = country_schema.dump(country)
    return jsonify({"data": data})

# Add a country
@api.route('', methods=['POST'])
def add_country():
    country_schema = CountrySchema()
    
    country_data = country_schema.load(request.get_json()) 
    db.session.add(country_data)
    db.session.commit()

    response_data = country_schema.dump(country_data)
    return jsonify({"data": response_data})
    
# Delete a country
@api.route('/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    country = Country.query.get(country_id)
    if not country:
        raise BadRequest("resource not found")
    
    db.session.delete(country)
    db.session.commit()

    return jsonify({'success': True})

# edit a country
@api.route('/<int:country_id>', methods=['PUT'])
def edit_country(country_id):
    country = Country.query.get(country_id)
    
    if not country:
        raise BadRequest("resource not found")

    country_loader = CountryLoader(partial=True)
    country_schema = CountrySchema()
    
    request_data = request.get_json()
    validated_data = country_loader.load(request_data,instance=country, partial=True)
    
    db.session.merge(validated_data)
    db.session.commit()

    updated_country_data = country_schema.dump(country)
    return jsonify({"data": updated_country_data})