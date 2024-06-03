from flask import Blueprint
from models.city import City, CitySchema, CityLoader
from models.state import State
from models.country import Country
from werkzeug.exceptions import BadRequest
from rest_framework.resource_api import ResourceAPI

api = Blueprint('city_api_v2', __name__)

class CityAPI(ResourceAPI):
    model_class = City
    schema_class = CitySchema
    loader_class = CityLoader

    def before_post(self, body):
        state_id = body.get('state_id')
        state = State.query.get(state_id)
        if not state:
            raise BadRequest('state does not exist')
        country = Country.query.get(state.country_id)
        body['country_id'] = country.id
        return body

# Register the views
city_view = CityAPI.as_view('city_api_v2')

# Add routes to the blueprint
api.add_url_rule('/cities', defaults={'resource_id': None}, view_func=city_view, methods=['GET'])
api.add_url_rule('/cities', view_func=city_view, methods=['POST'])
api.add_url_rule('/cities/<int:resource_id>', view_func=city_view, methods=['GET', 'PUT', 'DELETE'])
