"""This module contains the base class for all "services". A service is simply
the REST endpoints for a given ORM model (i.e. database table)."""

# Third-party imports
from flask import jsonify, request, make_response
from flask.views import MethodView

# Application imports
from sandman.model import db
from sandman.exception import NotFoundException


class Service(MethodView):
    """Base class for all resources."""

    __endpoint__ = ''
    __url__ = '/'
    __model__ = None

    def get(self, resource_id=None):
        """Return response to HTTP GET request.

        :param resource_id: Optional primary key value for resource.
        :rtype flask.Response:

        """

        if 'meta' in request.url:
            return self.meta()
        if resource_id is None:
            return self.all_resources()
        else:
            resource = self.resource(resource_id)
            if not resource:
                raise NotFoundException()
            return jsonify(resource.as_dict())

    def all_resources(self):
        """Return all resources of this type as a JSON list.

        :rtype flask.Response:

        """

        if 'page' not in request.args:
            resources = db.session.query(self.__model__).all()
        else:
            resources = self.__model__.query.paginate(
                int(request.args['page'])).items
        return jsonify(
            {self.__model__.__top_level_json_name__: [
                resource.as_dict() for resource in resources]})

    def post(self):
        """Return response to HTTP POST request.

        :rtype flask.Response:

        """

        resource = self.__model__.query.filter_by(**request.json).first()
        # resource already exists; don't create it again
        if resource:
            return self._no_content_response()
        instance = self.__model__(  # pylint: disable=not-callable
            **request.json)
        db.session.add(instance)
        db.session.commit()
        return self._created_response(instance)

    def delete(self, resource_id):
        """Return response to HTTP DELETE request.

        :rtype flask.Response:

        """

        instance = self.resource(resource_id)
        db.session.delete(instance)
        db.session.commit()
        return self._no_content_response()

    def put(self, resource_id):
        """Return response to HTTP PUT request.

        :param resource_id: Optional primary key value for resource.
        :rtype flask.Response:

        """

        instance = self.resource(resource_id)
        instance.replace(request.json)
        setattr(instance, instance.primary_key(), resource_id)
        db.session.add(instance)
        db.session.commit()
        return jsonify(instance.as_dict())

    def patch(self, resource_id):
        """Return response to HTTP PATCH request.

        :param resource_id: Optional primary key value for resource.
        :rtype flask.Response:

        """

        resource = self.resource(resource_id)
        resource.from_dict(request.json)
        db.session.add(resource)
        db.session.commit()
        return jsonify(resource.as_dict())

    def resource(self, resource_id):
        """Return resource represented by this *resource_id*.

        :param resource_id: Optional primary key value for resource.

        """

        return db.session.query(self.__model__).get(resource_id)

    def meta(self):
        """Return a description of the resource's fields and their associated
        types."""
        return jsonify(self.__model__.meta())

    @staticmethod
    def _no_content_response():
        """Return an HTTP 204 "No Content" response.

        :rtype flask.Response:

        """

        response = make_response()
        response.status_code = 204
        return response

    @staticmethod
    def _created_response(resource):
        """Return an HTTP 201 "Created" response.

        :rtype flask.Response:

        """

        response = jsonify(resource.as_dict())
        response.status_code = 201
        return response

    @classmethod
    def register_service(
            cls, app, primary_key='resource_id', primary_key_type='int'):
        """Register an API service endpoint.

        :param cls: The class to register
        :param app: An instance of a Flask application object
        :param str primary_key: The name of the instance field for this class
        :param str primary_key_type: The type (as a string) of the primary_key
                                     field

        """
        view_func = cls.as_view(cls.__endpoint__)  # pylint: disable=no-member
        methods = set(cls.__model__.__methods__)  # pylint: disable=no-member
        if 'GET' in methods:  # pylint: disable=no-member
            app.add_url_rule(
                cls.__url__, defaults={primary_key: None},
                view_func=view_func,
                methods=['GET'])
            app.add_url_rule(
                '{resource}/meta'.format(resource=cls.__url__),
                view_func=view_func,
                methods=['GET'])
        if 'POST' in methods:  # pylint: disable=no-member
            app.add_url_rule(
                cls.__url__, view_func=view_func, methods=['POST', ])

        app.add_url_rule(
            '{resource}/<{pk_type}:{pk}>'.format(
                resource=cls.__url__,
                pk=primary_key, pk_type=primary_key_type),
            view_func=view_func,
            methods=methods - set('POST'))
