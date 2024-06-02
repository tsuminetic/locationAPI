from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from models.city import City, CitySchema, CityLoader
from models.state import State
from models.country import Country
from werkzeug.exceptions import BadRequest

api = Blueprint('city_api', __name__)

class CityAPI(MethodView):

    def get(self, city_id=None):
        if city_id is None:
            # List all cities
            cities = City.query.all()
            city_schema = CitySchema(many=True)
            data = city_schema.dump(cities)
            return jsonify({"data": data, "metadata": {"total": len(cities)}})
        else:
            # Get a specific city
            city = City.query.get(city_id)
            if not city:
                raise BadRequest("resource not found")

            city_schema = CitySchema()
            data = city_schema.dump(city)
            return jsonify({"data": data})

    def post(self):
        # Add a city
        city_schema = CitySchema()

        try:
            city_data = city_schema.load(request.get_json())
        except ValidationError as err:
            raise BadRequest(err.messages)

        state_id = request.get_json().get('state_id')
        state = State.query.get(state_id)
        if not state:
            raise BadRequest('state does not exist')
        country = Country.query.get(state.country_id)

        city_data.country_id = country.id

        db.session.add(city_data)
        db.session.commit()

        response_data = city_schema.dump(city_data)
        return jsonify({"data": response_data})

    def delete(self, city_id):
        # Delete a city
        city = City.query.get(city_id)
        if not city:
            raise BadRequest("resource not found")

        db.session.delete(city)
        db.session.commit()

        return jsonify({'success': True})

    def put(self, city_id):
        # Edit a city
        city = City.query.get(city_id)
        if not city:
            raise BadRequest("City not found")

        city_loader = CityLoader(partial=True)
        city_schema = CitySchema(partial=True)

        request_data = request.get_json()
        try:
            validated_data = city_loader.load(request_data, instance=city, partial=True)
        except ValidationError as err:
            raise BadRequest(err.messages)

        db.session.merge(validated_data)
        db.session.commit()

        updated_city_data = city_schema.dump(city)
        return jsonify({"data": updated_city_data})

# Register the views
city_view = CityAPI.as_view('city_api')

# Add routes to the blueprint
api.add_url_rule('', defaults={'city_id': None}, view_func=city_view, methods=['GET'])
api.add_url_rule('', view_func=city_view, methods=['POST'])
api.add_url_rule('/<int:city_id>', view_func=city_view, methods=['GET', 'PUT', 'DELETE'])
