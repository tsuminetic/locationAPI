from apis.v2.city_api import api as city_api_v2
from apis.v2.state_api import api as state_api_v2
from apis.v2.country_api import api as country_api_v2

def initialize_routes_v2(app):
    app.register_blueprint(city_api_v2, url_prefix='/v2')
    app.register_blueprint(state_api_v2, url_prefix='/v2')
    app.register_blueprint(country_api_v2, url_prefix='/v2')