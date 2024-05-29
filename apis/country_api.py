from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from models.country import Country, CountrySchema, CountryLoader
from werkzeug.exceptions import BadRequest

api = Blueprint('country_api', __name__)

class CountryAPI(MethodView):

    def get(self, country_id=None):
        if country_id is None:
            # List all countries
            countries = Country.query.all()
            country_schema = CountrySchema(many=True)
            data = country_schema.dump(countries)
            return jsonify({"data": data, "metadata": {"total": len(countries)}})
        else:
            # Get a specific country
            country = Country.query.get(country_id)
            if not country:
                raise BadRequest("resource not found")

            country_schema = CountrySchema()
            data = country_schema.dump(country)
            return jsonify({"data": data})

    def post(self):
        # Add a country
        country_schema = CountrySchema()

        try:
            country_data = country_schema.load(request.get_json())
        except ValidationError as err:
            raise BadRequest(err.messages)
        
        db.session.add(country_data)
        db.session.commit()

        response_data = country_schema.dump(country_data)
        return jsonify({"data": response_data})

    def delete(self, country_id):
        # Delete a country
        country = Country.query.get(country_id)
        if not country:
            raise BadRequest("resource not found")
        
        db.session.delete(country)
        db.session.commit()

        return jsonify({'success': True})

    def put(self, country_id):
        # Edit a country
        country = Country.query.get(country_id)
        
        if not country:
            raise BadRequest("resource not found")

        country_loader = CountryLoader(partial=True)
        country_schema = CountrySchema()
        
        request_data = request.get_json()
        try:
            validated_data = country_loader.load(request_data, instance=country, partial=True)
        except ValidationError as err:
            raise BadRequest(err.messages)
        
        db.session.merge(validated_data)
        db.session.commit()

        updated_country_data = country_schema.dump(country)
        return jsonify({"data": updated_country_data})

# Register the views
country_view = CountryAPI.as_view('country_api')

# Add routes
api.add_url_rule('', defaults={'country_id': None}, view_func=country_view, methods=['GET'])
api.add_url_rule('', view_func=country_view, methods=['POST'])
api.add_url_rule('/<int:country_id>', view_func=country_view, methods=['GET', 'PUT', 'DELETE'])
