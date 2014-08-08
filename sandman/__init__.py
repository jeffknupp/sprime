from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeferredReflection

from sandman.model import db, Model
from sandman.service import Service

DeclarativeBase = declarative_base(cls=(Model, DeferredReflection))
Model = automap_base(DeclarativeBase)

def reflect_all_app(database_uri):
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
