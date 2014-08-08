"""Sandman allows you to automatically create a REST API service from a legacy
database."""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeferredReflection

from sandman.model import db, Model
from sandman.service import Service

__version__ = '0.0.1'
__all__ = ['Model', 'reflect_all_app']

Model = automap_base(declarative_base(cls=(Model, db.Model, DeferredReflection)))


def reflect_all_app(database_uri):
    """Return a Flask application object with all of the tables in
    *database_uri* automatically added as REST endpoints.

    :param str database_uri: The SQLAlchemy database URI to reflect

    """

    from sandman.application import app
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)
    with app.app_context():
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
            app.class_references[cls.__table__.name] = cls
            service_cls.register_service(app)
    return app
