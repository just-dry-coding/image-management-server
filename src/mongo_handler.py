from pymongo import MongoClient

from gridfs import GridFS


from os import path
import sys

from typing import NewType, Callable, List, Tuple


def _on_connect_default(connected, error_msg):
    if connected:
        print('mongo handler connected successfully')
    else:
        print(f'failed to connect mongo handler because: {error_msg}')


ConnectCallback = NewType('ConnectCallback', Callable[[bool, str], None])


class MongoHandler():
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
        return [f.id() for f in files]

    def get_file_by_id(self, file_id: str) -> Tuple[str, bytes]:
        file = fs.get(file_id)
        return (file.filename, file.read())

    def _check_connection(self, on_connect):
        try:
            _ = self.client.server_info()
            on_connect(True, '')
        except PyMongoError as e:
            on_connect(False, str(e))


def main(connection_string, database, collection):
    mongo_handler = MongoHandler(connection_string, database, collection)
    image_ids = mongo_handler.get_all_image_ids(collection)
    for id in image_ids:
        file = mongo_handler.get_file_by_id(id)
        with open(file.filename, "wb") as f:
            f.write(file.content)


if __name__ == '__main__':
    connection_string = sys.argv[1]
    database = sys.argv[2]
    collection = sys.argv[3]
    main(connection_string, database, collection)
