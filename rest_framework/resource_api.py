from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask.views import MethodView
from app import db
from werkzeug.exceptions import BadRequest

class ResourceAPI(MethodView):
    model_class = None
    schema_class = None
    loader_class = None

    def get(self, resource_id=None):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if resource_id is None:
            # List all resources
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
