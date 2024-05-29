from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from models.state import State, StateSchema, StateLoader
from models.country import Country
from werkzeug.exceptions import BadRequest

api = Blueprint('state_api', __name__)

class StateAPI(MethodView):

    def get(self, state_id=None):
        if state_id is None:
            # List all states
            states = State.query.all()
            state_schema = StateSchema(many=True)
            data = state_schema.dump(states)
            return jsonify({"data": data, "metadata": {"total": len(states)}})
        else:
            # Get a specific state
            state = State.query.get(state_id)
            if not state:
                raise BadRequest("resource not found")

            state_schema = StateSchema()
            data = state_schema.dump(state)
            return jsonify({"data": data})

    def post(self):
        # Add a state
        state_schema = StateSchema()

        try:
            state_data = state_schema.load(request.get_json())
        except ValidationError as err:
            raise BadRequest(err.messages)

        country_id = request.get_json().get('country_id')
        country = Country.query.get(country_id)
        if not country:
            raise BadRequest('Country does not exist')

        db.session.add(state_data)
        db.session.commit()

        response_data = state_schema.dump(state_data)
        return jsonify({"data": response_data})

    def delete(self, state_id):
        # Delete a state
        state = State.query.get(state_id)
        if not state:
            raise BadRequest("resource not found")

        db.session.delete(state)
        db.session.commit()

        return jsonify({'success': True})

    def put(self, state_id):
        # Edit a state
        state = State.query.get(state_id)
        if not state:
            raise BadRequest("State not found")

        state_loader = StateLoader(partial=True)
        state_schema = StateSchema(partial=True)

        request_data = request.get_json()
        try:
            validated_data = state_loader.load(request_data, instance=state, partial=True)
        except ValidationError as err:
            raise BadRequest(err.messages)

        db.session.merge(validated_data)
        db.session.commit()

        updated_state_data = state_schema.dump(state)
        return jsonify({"data": updated_state_data})

# Register the views
state_view = StateAPI.as_view('state_api')

# Add routes to the blueprint
api.add_url_rule('', defaults={'state_id': None}, view_func=state_view, methods=['GET'])
api.add_url_rule('', view_func=state_view, methods=['POST'])
api.add_url_rule('/<int:state_id>', view_func=state_view, methods=['GET', 'PUT', 'DELETE'])
