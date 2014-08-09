"""Sandman allows you to automatically create a REST API service from a legacy
database."""

from flask import jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeferredReflection
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from sandman.model import db, Model
from sandman.exception import (
    BadRequestException,
    ForbiddenException,
    NotAcceptableException,
    NotFoundException,
    ConflictException,
    ServerErrorException,
    NotImplementedException,
    ServiceUnavailableException,
    )
from sandman.service import Service

__version__ = '0.0.1'
__all__ = ['Model', 'reflect_all_app']

Model = automap_base(declarative_base(cls=(Model, db.Model, DeferredReflection)))


def reflect_all_app(database_uri):
    """Return a Flask application object with all of the tables in
    *database_uri* automatically added as REST endpoints.

    :param str database_uri: The SQLAlchemy database URI to reflect

    """

    from sandman.application import get_app
    app = get_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)
    with app.app_context():
        admin = Admin(app)
        app.class_references = {}
        Model.prepare(db.engine, reflect=True)
        for cls in Model.classes:
            service_cls = type(
                str(cls.__table__.name) + 'Service',
                (Service,),
                {
                    '__model__': cls,
                    '__endpoint__': str(cls.__table__.name),
                    '__url__': '/' + str(cls.__table__.name).lower()
                })
            admin.add_view(ModelView(cls, db.session))
            app.class_references[cls.__table__.name] = cls
            service_cls.register_service(app)

    @app.errorhandler(BadRequestException)
    @app.errorhandler(ForbiddenException)
    @app.errorhandler(NotAcceptableException)
    @app.errorhandler(NotFoundException)
    @app.errorhandler(ConflictException)
    @app.errorhandler(ServerErrorException)
    @app.errorhandler(NotImplementedException)
    @app.errorhandler(ServiceUnavailableException)
    def handle_application_error(error):
        """Handler used to send JSON error messages rather than default HTML
        ones."""
        response = jsonify(error.to_dict())
        response.status_code = error.code
        return response

    return app
