from flask import Blueprint
from models.state import State, StateSchema, StateLoader
from models.country import Country
from werkzeug.exceptions import BadRequest
from rest_framework.resource_api import ResourceAPI

api = Blueprint('state_api_v2', __name__)

class StateAPI(ResourceAPI):
    model_class = State
    schema_class = StateSchema
    loader_class = StateLoader

    def before_post(self, body):
        country_id = body.get('country_id')
        country = Country.query.get(country_id)
        if not country:
            raise BadRequest('country does not exist')
        return body

# Register the views
state_view = StateAPI.as_view('state_api_v2')

# Add routes to the blueprint
api.add_url_rule('/states', defaults={'resource_id': None}, view_func=state_view, methods=['GET'])
api.add_url_rule('/states', view_func=state_view, methods=['POST'])
api.add_url_rule('/states/<int:resource_id>', view_func=state_view, methods=['GET', 'PUT', 'DELETE'])
