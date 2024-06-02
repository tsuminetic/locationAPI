from apis.v2.resourse_api import api as ResourceAPI

def initialize_routes_v2(app):
    app.register_blueprint(ResourceAPI, url_prefix='/v2')