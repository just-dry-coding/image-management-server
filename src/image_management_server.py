from fastapi import FastAPI
from typing import List, Tuple

from .api_mongo_handler import ApiMongoHandler

class ImageManagementServer:
    def __init__(self, connection_string: str, database: str, collection: str):
        # get(/)        get all images
        # get(/id)      get specific image ??
        # delete(/id)   delete specific image
        # update(/id)   update specific image
        self.app = FastAPI()

        self.api_mongo_handler = ApiMongoHandler(connection_string, database, collection)

        self.setup_routs()

    def setup_routs(self):
        @self.app.get('/', response_model=List[str])
        async def get_all_ids(self):
            return self.api_mongo_handler.get_all_file_ids()
        
        @self.app.get('/id', response_model=[str, bytes])

