from apis.v1.country_api import api as country_api
from apis.v1.state_api import api as state_api
from apis.v1.city_api import api as city_api

def initialize_routes_v1(app):
    app.register_blueprint(country_api, url_prefix='/v1/countries')
    app.register_blueprint(state_api, url_prefix='/v1/states')
    app.register_blueprint(city_api, url_prefix='/v1/cities')