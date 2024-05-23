from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from models.state import State, StateSchema
from models.country import Country
from sqlalchemy.orm import joinedload

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
        return jsonify({'error': 'resource not found'}), 404

    state_schema = StateSchema()
    data = state_schema.dump(state)
    return jsonify({"data": data})

# Add a state
@api.route('', methods=['POST'])
def add_state():
    state_schema = StateSchema()

    country_name = request.json.get('country_name')
    country = Country.query.filter_by(name=country_name).first()
    if not country:
        return jsonify({'error': 'Country not found. Please add the country first.'}), 404
    
    try:
        state_data = state_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': 'please enter all fields correctly'}), 400

    state_data.country_id = country.id

    db.session.add(state_data)
    db.session.commit()

    response_data = state_schema.dump(state_data)
    return jsonify({"data": response_data})

# Delete a state
@api.route('/<int:state_id>', methods=['DELETE'])
def delete_country(state_id):
    state = State.query.get(state_id)
    if not state:
        return jsonify({'error': 'resource not found'}), 404
    
    db.session.delete(state)
    db.session.commit()

    return jsonify({'success': True})

# Edit a state
@api.route('/<int:state_id>', methods=['PUT'])
def edit_state(state_id):
    state = State.query.get(state_id)
    
    if not state:
        return jsonify({'error': 'State not found'}), 404

    state_schema = StateSchema(partial=True)
    
    try:
        request_data = request.get_json()
        validated_data = state_schema.load(request_data, partial=True)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    for key, value in request_data.items():
        if key == "id":
            return jsonify({'error': "Not allowed"}), 403
        setattr(state, key, value)

    db.session.commit()

    updated_state_data = state_schema.dump(state)
    return jsonify({"data": updated_state_data})
