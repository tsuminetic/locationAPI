from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from models.state import State,StateSchema, StateLoader
from models.country import Country
from werkzeug.exceptions import BadRequest

api = Blueprint('state_api', __name__)

# List all states
@api.route('')
def get_all():
    states = State.query.all()
    state_schema = StateSchema(many=True)
    data = state_schema.dump(states)
    return jsonify({"data": data, "metadata": {"total": len(states)}})

# Get a specific state
@api.route('/<int:state_id>')
def get_state(state_id):
    state = State.query.get(state_id)
    if not state:
        raise BadRequest("resource not found")

    state_schema = StateSchema()
    data = state_schema.dump(state)
    return jsonify({"data": data})
    
    
# Add a state
@api.route('', methods=['POST'])
def add_state():
    state_schema = StateSchema()
        
    state_data = state_schema.load(request.get_json())
    
    country_id = request.get_json().get('country_id')
    country = Country.query.get(country_id)
    if not country:
        raise BadRequest('Country does not exist')
    
    db.session.add(state_data)
    db.session.commit()

    response_data = state_schema.dump(state_data)
    return jsonify({"data": response_data})


# Delete a state
@api.route('/<int:state_id>', methods=['DELETE'])
def delete_country(state_id):
    state = State.query.get(state_id)
    if not state:
        raise BadRequest("resource not found")
    
    db.session.delete(state)
    db.session.commit()

    return jsonify({'success': True})
    
# Edit a state
@api.route('/<int:state_id>', methods=['PUT'])
def edit_state(state_id):

    state = State.query.get(state_id)

    if not state:
        raise BadRequest("State not found")

    state_loader = StateLoader(partial=True)
    state_schema = StateSchema(partial=True)
    
    request_data = request.get_json()

    validated_data = state_loader.load(request_data, instance=state, partial=True)
    db.session.merge(validated_data)
    db.session.commit()

    updated_state_data = state_schema.dump(state)
    return jsonify({"data": updated_state_data})