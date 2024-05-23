from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from models.country import Country, CountrySchema

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
        return jsonify({'error': 'resource not found'}), 404

    country_schema = CountrySchema()
    data = country_schema.dump(country)
    return jsonify({"data": data})

# Add a country
@api.route('', methods=['POST'])
def add_country():
    country_schema = CountrySchema()

    try:
        country_data = country_schema.load(request.get_json()) 
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    db.session.add(country_data)
    db.session.commit()

    response_data = country_schema.dump(country_data)
    return jsonify({"data": response_data})

# Delete a country
@api.route('/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    country = Country.query.get(country_id)
    if not country:
        return jsonify({'error': 'resource not found'}), 404
    
    db.session.delete(country)
    db.session.commit()

    return jsonify({'success': True})

# edit a country
@api.route('/<int:country_id>', methods=['PUT'])
def edit_country(country_id):
    country = Country.query.get(country_id)
    
    if not country:
        return jsonify({'error': 'Country not found'}), 404

    country_schema = CountrySchema(partial=True)
    
    try:
        request_data = request.get_json()
        validated_data = country_schema.load(request_data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    for key, value in request_data.items():
        if key=="id":
            return jsonify({'error': "not allowed"}), 403
        setattr(country, key, value)

    db.session.commit()

    updated_country_data = country_schema.dump(country)
    return jsonify({"data": updated_country_data})