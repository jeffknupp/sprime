"""Main test class for sandman"""
from __future__ import absolute_import
import sys

import json
import os
import shutil

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

print sys.path
from sandman import (
    reflect_all_app,
    custom_class_app
    )


@pytest.yield_fixture(scope='function')  # pylint: disable=no-member
def app():
    """Return the test application instance."""
    shutil.copy2(
        os.path.join('tests', 'data', 'chinook.sqlite3'), 'chinook.sqlite3')
    application = reflect_all_app('sqlite+pysqlite:///chinook.sqlite3')
    application.testing = True

    yield application.test_client()

    os.unlink('chinook.sqlite3')


@pytest.yield_fixture(scope='function')  # pylint: disable=no-member
def full_app():
    """Return the test application instance."""
    shutil.copy2(
        os.path.join('tests', 'data', 'chinook.sqlite3'), 'chinook.sqlite3')
    application = reflect_all_app('sqlite+pysqlite:///chinook.sqlite3')
    application.testing = True

    yield application

    os.unlink('chinook.sqlite3')


@pytest.yield_fixture(scope='function')  # pylint: disable=no-member
def custom_app():
    """Return the test application instance."""
    shutil.copy2(
        os.path.join('tests', 'data', 'chinook.sqlite3'), 'chinook.sqlite3')
    import models
    application = custom_class_app('sqlite+pysqlite:///chinook.sqlite3')
    application.testing = True

    yield application.test_client()

    os.unlink('chinook.sqlite3')


def test_get_resource(app):  # pylint: disable=redefined-outer-name
    """Can we GET a simple resource?"""
    response = app.get('/artist/1')

    assert response.status_code == 200
    resource = json.loads(response.get_data(as_text=True))
    assert resource['Name'] == 'AC/DC'


def test_get_collection(app):  # pylint: disable=redefined-outer-name
    """Can we GET a collection of resources?"""
    response = app.get('/artist')

    assert response.status_code == 200
    collection = json.loads(response.get_data(as_text=True))
    assert len(collection['resources']) == 275


def test_add_resource(app):  # pylint: disable=redefined-outer-name
    """Can we POST a new resource?"""
    response = app.post(
        '/artist',
        data=json.dumps({
            'Name': 'Jeff Knupp',
            'ArtistId': 276
            }),
        headers={'Content-type': 'application/json'})

    assert response.status_code == 201
    resource = json.loads(response.get_data(as_text=True))
    assert resource['Name'] == 'Jeff Knupp'
    assert resource['ArtistId'] == 276


def test_delete_resource(app):  # pylint: disable=redefined-outer-name
    """Can we DELETE a resource?"""
    response = app.delete('/album/1')

    assert response.status_code == 204

    response = app.get('/album/1')

    assert response.status_code == 404


def test_patch_resource(app):  # pylint: disable=redefined-outer-name
    """Can we PATCH a resource?"""
    response = app.patch(
        '/artist/275',
        data=json.dumps({
            'Name': 'Jeff Knupp',
            }),
        headers={'Content-type': 'application/json'})

    assert response.status_code == 200

    response = app.get('/artist/275')
    resource = json.loads(response.get_data(as_text=True))
    assert resource['Name'] == 'Jeff Knupp'


def test_put_resource(app):  # pylint: disable=redefined-outer-name
    """Can we PUT a resource?"""
    response = app.put(
        '/track/1',
        data=json.dumps({
            'Name': 'Some Song',
            'AlbumId': 1,
            'MediaTypeId': 1,
            'GenreId': 1,
            'Milliseconds': 100,
            'UnitPrice': 10.99
            }),
        headers={'Content-type': 'application/json'})

    assert response.status_code == 200

    response = app.get('/track/1')
    resource = json.loads(response.get_data(as_text=True))
    assert resource['Name'] == 'Some Song'
    assert resource['Bytes'] is None


def test_meta_endpoint(app):  # pylint: disable=redefined-outer-name
    """Can we get the meta-endpoint of a resource?"""
    response = app.get('/artist/meta')

    assert response.status_code == 200
    resource_description = json.loads(response.get_data(as_text=True))
    assert resource_description['Artist']['ArtistId'] == 'integer'


def test_pagination(app):  # pylint: disable=redefined-outer-name
    """Can we properly paginate a collection?"""
    response = app.get('/artist?page=1')

    assert response.status_code == 200
    collection = json.loads(response.get_data(as_text=True))
    assert len(collection['resources']) == 20


def test_post_existing_resource(app):  # pylint: disable=redefined-outer-name
    """Do we properly ignore POSTing an existing resource?"""
    response = app.post(
        '/artist',
        data=json.dumps({
            'Name': 'Philip Glass Ensemble',
            'ArtistId': 275
            }),
        headers={'Content-type': 'application/json'})

    assert response.status_code == 204


def test_custom_class_app_get(custom_app):
    """Can we successfully get a resource using custom models?"""
    response = custom_app.get('/artist/1')

    assert response.status_code == 200
