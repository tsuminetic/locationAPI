from apis.country_api import api as country_api
from apis.state_api import api as state_api
from apis.city_api import api as city_api

def initialize_routes(app):
    app.register_blueprint(country_api, url_prefix='/countries')
    app.register_blueprint(state_api, url_prefix='/states')
    app.register_blueprint(city_api, url_prefix='/cities')