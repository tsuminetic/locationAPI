from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from models.city import City, CitySchema, CityLoader
from models.state import State, StateSchema, StateLoader
from models.country import Country, CountrySchema, CountryLoader
from werkzeug.exceptions import BadRequest

api = Blueprint('resource_api', __name__)

class ResourceAPI(MethodView):
    model_class = None
    schema_class = None
    loader_class = None

    def get(self, resource_id=None):
        if resource_id is None:
            # List all resources
            resources = self.model_class.query.all()
            schema = self.schema_class(many=True)
            data = schema.dump(resources)
            return jsonify({"data": data, "metadata": {"total": len(resources)}})
        else:
            # Get a specific resource
            resource = self.model_class.query.get(resource_id)
            if not resource:
                raise BadRequest("resource not found")

            schema = self.schema_class()
            data = schema.dump(resource)
            return jsonify({"data": data})

    def before_post(self, body):
        return body

    def after_post(self, resource):
        pass

    def post(self):
        # Add a resource
        schema = self.schema_class()

        body = self.before_post(request.get_json())
        try:
            resource_data = schema.load(body)
        except ValidationError as err:
            raise BadRequest(err.messages)

        db.session.add(resource_data)
        db.session.commit()

        self.after_post(resource_data)

        response_data = schema.dump(resource_data)
        return jsonify({"data": response_data})

    def delete(self, resource_id):
        # Delete a resource
        resource = self.model_class.query.get(resource_id)
        if not resource:
            raise BadRequest("resource not found")

        db.session.delete(resource)
        db.session.commit()

        return jsonify({'success': True})

    def put(self, resource_id):
        # Edit a resource
        resource = self.model_class.query.get(resource_id)
        if not resource:
            raise BadRequest("resource not found")

        loader = self.loader_class(partial=True)
        schema = self.schema_class(partial=True)

        request_data = request.get_json()
        try:
            validated_data = loader.load(request_data, instance=resource, partial=True)
        except ValidationError as err:
            raise BadRequest(err.messages)

        db.session.merge(validated_data)
        db.session.commit()

        updated_resource_data = schema.dump(resource)
        return jsonify({"data": updated_resource_data})

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

class CountryAPI(ResourceAPI):
    model_class = Country
    schema_class = CountrySchema
    loader_class = CountryLoader

# Register the views
city_view = CityAPI.as_view('city_api')
state_view = StateAPI.as_view('state_api')
country_view = CountryAPI.as_view('country_api')

# Add routes to the blueprint
api.add_url_rule('/cities', defaults={'resource_id': None}, view_func=city_view, methods=['GET'])
api.add_url_rule('/cities', view_func=city_view, methods=['POST'])
api.add_url_rule('/cities/<int:resource_id>', view_func=city_view, methods=['GET', 'PUT', 'DELETE'])

api.add_url_rule('/states', defaults={'resource_id': None}, view_func=state_view, methods=['GET'])
api.add_url_rule('/states', view_func=state_view, methods=['POST'])
api.add_url_rule('/states/<int:resource_id>', view_func=state_view, methods=['GET', 'PUT', 'DELETE'])

api.add_url_rule('/countries', defaults={'resource_id': None}, view_func=country_view, methods=['GET'])
api.add_url_rule('/countries', view_func=country_view, methods=['POST'])
api.add_url_rule('/countries/<int:resource_id>', view_func=country_view, methods=['GET', 'PUT', 'DELETE'])
