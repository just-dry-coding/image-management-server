from pymongo import MongoClient
from pymongo.errors import PyMongoError

from gridfs import GridFS
from gridfs.errors import NoFile
import bson
import base64


import sys

from typing import NewType, Callable, List, Tuple


def _on_connect_default(connected, error_msg):
    if connected:
        print('mongo handler connected successfully')
    else:
        print(f'failed to connect mongo handler because: {error_msg}')


ConnectCallback = NewType('ConnectCallback', Callable[[bool, str], None])


class ApiMongoHandler():
    """
        todo: docu write interface and methods
    """

    def __init__(self, connection_string: str, database: str, collection: str, on_connect: ConnectCallback = _on_connect_default):
        self.client = MongoClient(connection_string)
        self._check_connection(on_connect)
        self.database = self.client[database]
        self.fs = GridFS(self.database, collection=collection)

    def get_all_file_ids(self) -> List[str]:
        files = self.fs.find()
        # seems like I'm accessing a private field
        return [str(f._id) for f in files]

    def get_file_by_id(self, file_id: str) -> Tuple[str, str]:
        """
            throws bson.error.InvalidId for invalid file_id
            throws gridfs.errors.NoFile for file not found
        """
        file = self.fs.get(bson.ObjectId(file_id))
        return (file.filename, file.read())

    def update_file_by_id(self, file_id: str, filename: str, file: str) -> None:
        """
            throws bson.error.InvalidId for invalid file_id
            throws gridfs.errors.NoFile for file not found
        """
        file_id_bson = bson.ObjectId(file_id)
        if not self.fs.exists(file_id_bson):
            raise NoFile()
        # todo: not a safe way of updating -> need abondon gridfs to change
        self.fs.delete(file_id=file_id_bson)
        self.fs.put(file, _id=file_id_bson, filename=filename)

    def delete_file_by_id(self, file_id: str) -> None:
        """
            throws bson.error.InvalidId for invalid file_id
            throws gridfs.errors.NoFile for file not found
        """
        file_id_bson = bson.ObjectId(file_id)
        if not self.fs.exists(file_id_bson):
            raise NoFile()
        # todo: not a safe way of updating -> need abondon gridfs to change
        self.fs.delete(file_id=file_id_bson)

    def _check_connection(self, on_connect):
        try:
            _ = self.client.server_info()
            on_connect(True, '')
        except PyMongoError as e:
            on_connect(False, str(e))


def main(connection_string, database, collection):
    mongo_handler = ApiMongoHandler(connection_string, database, collection)
    image_ids = mongo_handler.get_all_image_ids(collection)
    for id in image_ids:
        [filename, data] = mongo_handler.get_file_by_id(id)
        with open(filename, "wb") as f:
            f.write(data)


if __name__ == '__main__':
    connection_string = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    main(connection_string, database, collection)
