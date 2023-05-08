from unittest import TestCase

from src.mongo_handler import MongoHandler

from os import environ, path


_connection_string = environ.get('TEST_DATABASE_CONNECTION_STRING')


@pytest.fixture(scope="session")
def mongo_handler():
    mongo_handler = MongoHandler(
        self._connection_string, 'test_api_server', test_callback)
    yield mongo_handler


class MongoHandlerTest(TestCase):
    def test_connect(self):
        def test_callback(connected, _):
            assert connected

        _ = MongoHandler(self._connection_string, '_', test_callback)

    def test_failed_connection(self):
        def test_callback(connected, _):
            assert not connected

        mongo_handler = MongoHandler('_', '_', test_callback)

        assert mongo_handler != None

    @pytest.mark.usefixtures("mongo_handler")
    def test_retreive_all_images(self):
        images = mongo_handler.retreive_all_images('test')
        assert len(images) == 1
        for image in images:
            pass
