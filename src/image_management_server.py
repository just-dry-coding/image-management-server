# quickfix includes
import sys  # noqa
from os import path  # noqa

current_directory = path.dirname(path.abspath(__file__))  # noqa
sys.path.append(current_directory)  # noqa

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Tuple

import uvicorn

from api_mongo_handler import ApiMongoHandler


origins = [
    "http://localhost:3000/",
    "localhost:3000"
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # todo: set proper origins
    allow_credentials=True,
    allow_methods=["GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

connection_string = sys.argv[1]
database = sys.argv[2]
collection = sys.argv[3]
api_mongo_handler = ApiMongoHandler(
    connection_string, database, collection)


@app.options("/images/{id}")
async def options_images(id: str):
    return {"Allow": "OPTIONS, PUT, GET, DELETE"}


@app.get('/images', response_model=List[str])
async def get_all_image_ids():
    response = api_mongo_handler.get_all_file_ids()
    return response


@app.get('/images/{id}', response_model=Tuple[str, str])
async def get_image_by_id(id: str):
    print(id)
    [filename, file] = api_mongo_handler.get_file_by_id(id)
    content_type = "application/octet-stream"
    response = StreamingResponse(iter([file]), media_type=content_type)
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@app.put('/images/{id}')
async def edit_image(id: str,  file: UploadFile = File(...)):
    filename = file.filename
    file_data = await file.read()
    api_mongo_handler.update_file_by_id(id, filename, file_data)
    return {"message": "Image edited successfully"}


@app.delete('/images/{id}')
async def edit_image(id: str):
    api_mongo_handler.delete_file_by_id(id)
    return {"message": "Image deleted successfully"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
