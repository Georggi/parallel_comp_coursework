from multiprocessing import Manager, Pool, Lock


class Database:
    """Class that handles storage for inverted index"""
    def __init__(self, manager: Manager):
        """Initialize database dict with process-safe dictionary"""
        self.__db = manager.dict()
        self.__db_lock = Lock()

    def __getitem__(self, item: str):
        """Implement magic for getting item from index by key
           :item - key word for search"""

        return self.__db.get(item, None)

    def insert(self, item):
        self.__db.update()

    def remove(self, item):
        return self.__db.pop(None, None)
