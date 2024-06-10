from flask import Blueprint
from models.country import Country, CountrySchema, CountryLoader
from rest_framework.resource_api import ResourceAPI

api = Blueprint('country_api_v2', __name__)

class CountryAPI(ResourceAPI):
    model_class = Country
    schema_class = CountrySchema
    loader_class = CountryLoader
    
    def order_query(self, query, query_params):
        order_by_mappings = {
            'name': self.model_class.name,
            'capital': self.model_class.capital,
            'population': self.model_class.population,
            'continent': self.model_class.continent,
            'iso_code': self.model_class.iso_code,
            'id': self.model_class.id
        }

        order_by = query_params.get('order_by')
        order_direction = query_params.get('order_direction', 'asc')  # Default to ascending order

        if order_by in order_by_mappings:
            field = order_by_mappings[order_by]
            if order_direction == 'desc':
                field = field.desc()
            query = query.order_by(field)

        return query

    
    def filter_query(self, query, query_params):
        filters = {
            'name': lambda value: self.model_class.name.like(f"%{value}%"),
            'capital': lambda value: self.model_class.capital.like(f"%{value}%"),
            'population_min': lambda value: self.model_class.population >= int(value),
            'population_max': lambda value: self.model_class.population <= int(value),
            'continent': lambda value: self.model_class.continent.like(f"%{value}%"),
            'iso_code': lambda value: self.model_class.iso_code.like(f"%{value}%"),
        }

        for param, value in query_params.items():
            if param in filters:
                query = query.filter(filters[param](value))
        return query
    
# Register the views
country_view = CountryAPI.as_view('country_api_v2')

# Add routes to the blueprint
api.add_url_rule('/countries', defaults={'resource_id': None}, view_func=country_view, methods=['GET'])
api.add_url_rule('/countries', view_func=country_view, methods=['POST'])
api.add_url_rule('/countries/<int:resource_id>', view_func=country_view, methods=['GET', 'PUT', 'DELETE'])
api.add_url_rule('/countries/search', view_func=country_view, methods=['GET'], endpoint='search')