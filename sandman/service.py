from flask import jsonify, request, make_response
from flask.views import MethodView

from sandman.model import db
from sandman.exception import NotFoundException


class Service(MethodView):
    """Base class for all resources."""

    __endpoint__ = ''
    __url__ = '/'
    __model__ = None

    def get(self, resource_id=None):
        """Return response to HTTP GET request."""
        if resource_id is None:
            return self.all_resources()
        else:
            resource = self.resource(resource_id)
            if not resource:
                raise NotFoundException()
            return jsonify(resource.as_dict())

    def all_resources(self):
        """Return all resources of this type as a JSON list."""
        if 'page' not in request.args:
            resources = db.session.query(self.__model__).all()
        else:
            resources = self.__model__.query.paginate(
                int(request.args['page'])).items
        return jsonify(
            {'resources': [resource.as_dict() for resource in resources]})

    def post(self):
        """Return response to HTTP POST request."""
        resource = self.__model__.query.filter_by(**request.json).first()
        # resource already exists; don't create it again
        if resource:
            return self._no_content_response()
        instance = self.__model__(**request.json)
        self.record_action('CREATE')
        db.session.add(instance)
        db.session.commit()
        return jsonify(instance.as_dict())

    def delete(self, resource_id):
        """Return response to HTTP DELETE request."""
        instance = self.resource(resource_id)
        self.record_action('DELETE')
        db.session.delete(instance)
        db.session.commit()
        return self._no_content_response()

    def put(self, resource_id):
        """Return response to HTTP PUT request."""
        instance = self.resource(resource_id)
        if instance is None:
            instance = self.__model__(**request.json)
            self.record_action('CREATE')
        else:
            instance.from_dict(request.json)
            self.record_action('UPDATE')
        db.session.add(instance)
        db.session.commit()
        return jsonify(instance.as_dict())

    def patch(self, resource_id):
        """Return response to HTTP PATCH request."""
        resource = self.resource(resource_id)
        resource.from_dict(request.json)
        db.session.add(resource)
        db.session.commit()
        return jsonify(resource.as_dict())

    def resource(self, resource_id):
        """Return resource represented by this *resource_id*."""
        return db.session.query(self.__model__).get(resource_id)

    @staticmethod
    def _no_content_response():
        """Return an HTTP 204 "No Content" response."""
        response = make_response()
        response.status_code = 204
        return response

    @staticmethod
    def _created_response(resource):
        """Return an HTTP 201 "Created" response."""
        response = jsonify(resource)
        response.status_code = 201
        return response

    @classmethod
    def register_service(cls, app, primary_key='resource_id', primary_key_type='int'):
        """Register an API service endpoint."""
        view_func = cls.as_view(cls.__endpoint__)
        app.add_url_rule(
            cls.__url__, defaults={primary_key: None},
            view_func=view_func,
            methods=['GET'])
        app.add_url_rule(cls.__url__, view_func=view_func, methods=['POST', ])
        app.add_url_rule(
            '{resource}/<{pk_type}:{pk}>'.format(
                resource=cls.__url__,
                pk=primary_key, pk_type=primary_key_type),
            view_func=view_func,
            methods=['GET', 'PUT', 'PATCH', 'DELETE'])
