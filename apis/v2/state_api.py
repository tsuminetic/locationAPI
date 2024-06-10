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

    def filter_query(self, query, query_params):
        filters = {
            'name': lambda value: self.model_class.name.like(f"%{value}%"),
            'population_min': lambda value: self.model_class.population >= int(value),
            'population_max': lambda value: self.model_class.population <= int(value),
        }

        for param, value in query_params.items():
            if param in filters:
                query = query.filter(filters[param](value))
            elif param == 'country_name':
                query = query.join(Country).filter(Country.name.like(f"%{value}%"))
                
        return query
    
    def order_query(self, query, query_params):
        order_by_mappings = {
            'name': self.model_class.name,
            'population': self.model_class.population,
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
state_view = StateAPI.as_view('state_api_v2')

# Add routes to the blueprint
api.add_url_rule('/states', defaults={'resource_id': None}, view_func=state_view, methods=['GET'])
api.add_url_rule('/states', view_func=state_view, methods=['POST'])
api.add_url_rule('/states/<int:resource_id>', view_func=state_view, methods=['GET', 'PUT', 'DELETE'])
api.add_url_rule('/states/search', view_func=state_view, methods=['GET'], endpoint='search')