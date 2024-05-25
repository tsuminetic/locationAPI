from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from models.city import City, CitySchema, CityLoader
from models.state import State
from models.country import Country
from werkzeug.exceptions import BadRequest

api = Blueprint('city_api',__name__)

# List all cities
@api.route('')
def get_all():
    cities = City.query.all()
    city_schema = CitySchema(many=True)
    data = city_schema.dump(cities)
    return jsonify({"data": data, "metadata": {"total": len(cities)}})

# Get a specific city
@api.route('/<int:city_id>')
def get_city(city_id):
    try:
        city = City.query.get(city_id)
        if not city:
            raise BadRequest("resource not found")

        city_schema = CitySchema()
        data = city_schema.dump(city)
        return jsonify({"data": data})
    except BadRequest as err: 
        return jsonify({'error': str(err)}), 400 
    
# Add a city
@api.route('', methods=['POST'])
def add_city():
    city_schema = CitySchema()
    
    try:
        
        city_data = city_schema.load(request.get_json())
        
        state_id = request.get_json().get('state_id')
        state = State.query.get(state_id)
        if not state:
            raise BadRequest('state does not exist')
        country = Country.query.get(state.country_id)

        city_data.country_id = country.id
        
        db.session.add(city_data)
        db.session.commit()

        response_data = city_schema.dump(city_data)
        return jsonify({"data": response_data})
    except ValidationError as err:
        return jsonify({'error': 'please enter all fields correctly'}), 400
    except BadRequest as err: 
        return jsonify({'error': str(err)}), 400 
    
# Delete a state
@api.route('/<int:city_id>', methods=['DELETE'])
def delete_country(city_id):
    try:
        city = City.query.get(city_id)
        if not city:
            raise BadRequest("resource not found")
        
        db.session.delete(city)
        db.session.commit()

        return jsonify({'success': True})
    except BadRequest as err: 
        return jsonify({'error': str(err)}), 400 
    
    
# Edit a state
@api.route('/<int:state_id>', methods=['PUT'])
def edit_state(state_id):
    
    try:
        city = City.query.get(state_id)
    
        if not city:
            raise BadRequest("State not found")

        city_loader = CityLoader(partial=True)
        city_schema = CitySchema(partial=True)
        
        request_data = request.get_json()

        validated_data = city_loader.load(request_data, instance=city, partial=True)
        db.session.merge(validated_data)
        db.session.commit()

        updated_state_data = city_schema.dump(city)
        return jsonify({"data": updated_state_data})
    
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except ZeroDivisionError as err:
        return jsonify({'error': err.args[0]}), 500
    except BadRequest as err:
        return jsonify({'error': str(err)}), 400 
    except Exception as err:
        return jsonify({'error': err.args[0]}), 500