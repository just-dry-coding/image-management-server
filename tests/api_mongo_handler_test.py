import pytest

from src.api_mongo_handler import ApiMongoHandler
import bson
from gridfs.errors import NoFile

from os import environ, path

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
    assert filename == 'image1.jpg'


@pytest.mark.usefixtures("mongo_handler")
def test_update_file_by_id(mongo_handler):
    image_ids = mongo_handler.get_all_file_ids()
    assert len(image_ids) == 1
    current_dir = path.dirname(path.abspath(__file__))
    _filename = 'image2.jpg'
    with open(path.join(current_dir, 'test_images', _filename), 'rb') as file:
        mongo_handler.update_file_by_id(image_ids[0], _filename, file)
    [filename, _] = mongo_handler.get_file_by_id(image_ids[0])
    assert filename == "image2.jpg"
    # clean up
    _filename = 'image1.jpg'
    with open(path.join(current_dir, 'test_images', _filename), 'rb') as file:
        mongo_handler.update_file_by_id(image_ids[0], _filename, file)


@pytest.mark.usefixtures("mongo_handler")
def test_delete_file_by_id(mongo_handler):
    image_ids = mongo_handler.get_all_file_ids()
    assert (len(image_ids) == 1)
    mongo_handler.delete_file_by_id(image_ids[0])
    image_ids_after = mongo_handler.get_all_file_ids()
    assert (len(image_ids_after) == 0)
    # clean up
    current_dir = path.dirname(path.abspath(__file__))
    filename = 'image1.jpg'
    with open(path.join(current_dir, 'test_images', filename), 'rb') as file:
        mongo_handler._fs.put(file, _id=bson.ObjectId(
            image_ids[0]), filename=filename)


@pytest.mark.usefixtures("mongo_handler")
def test_get_file_by_invalid_id(mongo_handler):
    with pytest.raises(bson.errors.InvalidId):
        [_, _] = mongo_handler.get_file_by_id('some_invalid_id+#')


@pytest.mark.usefixtures("mongo_handler")
def test_get_file_where_image_not_found(mongo_handler):
    with pytest.raises(NoFile):
        randomId = bson.ObjectId()
        [_, _] = mongo_handler.get_file_by_id(randomId)


@pytest.mark.usefixtures("mongo_handler")
def test_update_file_where_image_not_found(mongo_handler):
    with pytest.raises(NoFile):
        randomId = bson.ObjectId()
        mongo_handler.update_file_by_id(randomId, '_', '_')


@pytest.mark.usefixtures("mongo_handler")
def test_update_file_by_invalid_id(mongo_handler):
    with pytest.raises(bson.errors.InvalidId):
        mongo_handler.update_file_by_id('some_invalid_id+#', '_', '_')
