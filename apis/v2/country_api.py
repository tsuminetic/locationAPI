from flask import Blueprint
from models.country import Country, CountrySchema, CountryLoader
from rest_framework.resource_api import ResourceAPI

api = Blueprint('country_api_v2', __name__)

class CountryAPI(ResourceAPI):
    model_class = Country
    schema_class = CountrySchema
    loader_class = CountryLoader

# Register the views
country_view = CountryAPI.as_view('country_api_v2')

# Add routes to the blueprint
api.add_url_rule('/countries', defaults={'resource_id': None}, view_func=country_view, methods=['GET'])
api.add_url_rule('/countries', view_func=country_view, methods=['POST'])
api.add_url_rule('/countries/<int:resource_id>', view_func=country_view, methods=['GET', 'PUT', 'DELETE'])
