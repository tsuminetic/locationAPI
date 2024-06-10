from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from werkzeug.exceptions import BadRequest

class ResourceAPI(MethodView):
    model_class = None
    schema_class = None
    loader_class = None
    default_page_size = 10

    def filter_query(self, query):
        pass
    
    def order_query(self, query, query_params):
        pass

    def before_get(self):
        pass

    def after_get(self, data):
        pass
    
    def search(self):
        query_params = request.args
        query = self.model_class.query

        resources = self.filter_query(query, query_params).all()
        resources = self.order_query(query, query_params).all()
        schema = self.schema_class(many=True)
        data = schema.dump(resources)
        return jsonify({"data": data})
    
    def detail(self, resource_id):
        resource = self.model_class.query.get(resource_id)
        if not resource:
            raise BadRequest("Resource not found")

        schema = self.schema_class()
        data = schema.dump(resource)
        return jsonify({"data": data})

    def list(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', self.default_page_size, type=int)

        resources = self.model_class.query.paginate(page=page, per_page=per_page)
        schema = self.schema_class(many=True)
        data = schema.dump(resources.items)
        return jsonify({
            "data": data, 
            "metadata": {
                "total": resources.total,
                "page": page,
                "per_page": per_page
            }
        })

    def get(self, resource_id=None):
        self.before_get()
        if request.endpoint in {'country_api_v2.search', 'state_api_v2.search', 'city_api_v2.search'}:
            response = self.search()
        elif resource_id is None:
            response = self.list()
        else:
            response = self.detail(resource_id)
        self.after_get(response.json)
        return response

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
