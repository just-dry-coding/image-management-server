from fastapi.testclient import TestClient

# dirty hack to pass arguments to database:
import sys
from os import environ

sys.argv = ['_', environ.get(
    'TEST_DATABASE_CONNECTION_STRING'), 'test_api_server', 'test']

from src.image_management_server import app  # noqa

client = TestClient(app)


def test_read():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == ['test', 'test']
