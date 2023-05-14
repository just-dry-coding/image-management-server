from fastapi.testclient import TestClient

# dirty hack to pass arguments to database:
import sys
from os import environ

sys.argv = ['_', environ.get(
    'TEST_DATABASE_CONNECTION_STRING'), 'test_api_server', 'test']

from src.image_management_server import app  # noqa

client = TestClient(app)


def test_get_all_image_ids():
    response = client.get('/images')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_image_by_id():
    image_ids_response = client.get('/images')
    image_ids = image_ids_response.json()
    response = client.get(f'/images/{image_ids[0]}')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"

# todo: continue tests
# def test_edit_image():
#     response = client.put(f'/images/{image_id}', file=file)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Image edited successfully"}


# def test_delete_image():
#     response = client.delete(f'/images/{image_id}')
#     assert response.status_code == 200
#     assert response.json() == {"message": "Image deleted successfully"}
