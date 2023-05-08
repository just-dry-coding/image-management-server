from unittest import TestCase
import pytest

from src.api_mongo_handler import ApiMongoHandler

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
    images = mongo_handler.get_all_file_ids()
    [filename, _] = mongo_handler.get_file_by_id(images[0])
    assert filename == "image1.jpg"
