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
    
    def before_post(self, body):
        country_id = body.get('country_id')
        country = Country.query.get(country_id)
        if not country:
            raise BadRequest('country does not exist')
        return body

    def filter_query(self, query, query_params):
        filters = {
            'name': lambda value: self.model_class.name.like(f"%{value}%"),
            'postal_code': lambda value: self.model_class.postal_code.like(f"%{value}%"),
        }

        for param, value in query_params.items():
            if param in filters:
                query = query.filter(filters[param](value))
            elif param == 'country_name':
                query = query.join(Country).filter(Country.name.like(f"%{value}%"))
            elif param == 'state_name':
                query = query.join(State).filter(State.name.like(f"%{value}%"))
                
        return query
    
    def order_query(self, query, query_params):
        order_by_mappings = {
            'name': self.model_class.name,
            'postal_code': self.model_class.postal_code,
            'state_id': self.model_class.state_id,
            'country_id': self.model_class.country_id,
            'id': self.model_class.id
        }

        order_by = query_params.get('order_by')
        order_direction = query_params.get('order_direction', 'asc')
        if order_by in order_by_mappings:
            field = order_by_mappings[order_by]
            if order_direction == 'desc':
                field = field.desc()
            query = query.order_by(field)

        return query
    

# Register the views
city_view = CityAPI.as_view('city_api_v2')

# Add routes to the blueprint
api.add_url_rule('/cities', defaults={'resource_id': None}, view_func=city_view, methods=['GET'])
api.add_url_rule('/cities', view_func=city_view, methods=['POST'])
api.add_url_rule('/cities/<int:resource_id>', view_func=city_view, methods=['GET', 'PUT', 'DELETE'])
api.add_url_rule('/cities/search', view_func=city_view, methods=['GET'], endpoint='search')