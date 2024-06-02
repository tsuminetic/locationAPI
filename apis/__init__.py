from apis.resourse_api import api as ResourceAPI
    
from apis.country_api import api as country_api
from apis.state_api import api as state_api
from apis.city_api import api as city_api

def initialize_routes(app):
    app.register_blueprint(ResourceAPI, url_prefix='/v2')

    app.register_blueprint(country_api, url_prefix='/v1/countries')
    app.register_blueprint(state_api, url_prefix='/v1/states')
    app.register_blueprint(city_api, url_prefix='/v1/cities')