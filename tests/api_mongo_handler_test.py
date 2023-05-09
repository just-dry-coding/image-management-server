import pytest

from src.api_mongo_handler import ApiMongoHandler
import bson
from gridfs.errors import NoFile

from os import environ


_connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')


@pytest.fixture()
def mongo_handler():
    mongo_handler = ApiMongoHandler(
        _connection_string, 'test_api_server', 'test')
    yield mongo_handler


def test_connect():
    def test_callback(connected, _):
        assert connected

    _ = ApiMongoHandler(_connection_string, '_', '_', test_callback)


def test_failed_connection():
    def test_callback(connected, _):
        assert not connected

    mongo_handler = ApiMongoHandler('_', '_', '_', test_callback)

    assert mongo_handler != None


@pytest.mark.usefixtures("mongo_handler")
def test_get_all_file_ids(mongo_handler):
    images = mongo_handler.get_all_file_ids()
    assert len(images) == 1


@pytest.mark.usefixtures("mongo_handler")
def test_get_file_by_id(mongo_handler):
    image_ids = mongo_handler.get_all_file_ids()
    [filename, _] = mongo_handler.get_file_by_id(image_ids[0])
    assert filename == "image1.jpg"


@pytest.mark.usefixtures("mongo_handler")
def test_get_file_by_invalid_id(mongo_handler):
    with pytest.raises(bson.errors.InvalidId):
        [filename, _] = mongo_handler.get_file_by_id('some_invalid_id+#')


@pytest.mark.usefixtures("mongo_handler")
def test_get_file_where_image_not_found(mongo_handler):
    with pytest.raises(NoFile):
        randomId = bson.ObjectId()
        [filename, _] = mongo_handler.get_file_by_id(randomId)
