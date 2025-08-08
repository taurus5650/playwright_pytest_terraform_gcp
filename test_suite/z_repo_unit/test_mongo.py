import mongomock
from configparser import ConfigParser
from infra.mongo_database import PyMongoDB
from infra.config import get_env_config


class MockedPyMongoDB(PyMongoDB):
    def __init__(self, section: str = 'FUNC_DB_MOCK'):
        client = mongomock.MongoClient()
        super().__init__(section=section, client=client)
        self._config['DATABASE'] = 'testdb'
        self._db = client['testdb']


class TestCase:
    COLLECTION = "users"

    def setup_method(self):
        cfg = {'USER': 'u', 'PASSWORD': 'p', 'HOST': 'localhost', 'DATABASE': 'testdb'}
        client = mongomock.MongoClient()
        self.database = PyMongoDB(config=cfg, client=client)

    def teardown_method(self):
        self.database.close()

    def test_remove_empty_values(self):
        test_input = {
            "a": 123,
            "b": None,
            "c": "",
            "d": {
                "d1": None,
                "d2": "hi",
                "d3": {
                    "d31": "",
                    "d32": "ok"
                }
            },
            "e": {},
            "f": {
                "f1": "",
                "f2": None
            }
        }

        expected_output = {
            "a": 123,
            "d": {
                "d2": "hi",
                "d3": {
                    "d32": "ok"
                }
            }
        }

        result = self.database.remove_empty_values(condition=test_input)
        assert result == expected_output

    def test_insert_one(self):
        result = self.database.insert_one(
            collection_name=self.COLLECTION,
            document={"name": "Alice", "age": 30}
        )
        assert result.inserted_id is not None

    def test_read_one(self):
        self.database.insert_one(
            collection_name=self.COLLECTION,
            document={"name": "Bob", "age": 25}
        )

        result = self.database.read(
            collection_name=self.COLLECTION,
            query={"name": "Bob"}
        )
        assert result['age'] == 25

    def test_update_one(self):
        self.database.insert_one(
            collection_name=self.COLLECTION,
            document={"name": "Charlie", "age": 20}
        )

        result = self.database.update_one(
            collection_name=self.COLLECTION,
            filter_query={"name": "Charlie"},
            update_data={"$set": {"age": 21}}
        )
        assert result.modified_count == 1

        updated_doc = self.database.read(
            collection_name=self.COLLECTION,
            query={"name": "Charlie"})
        assert updated_doc['age'] == 21

    def test_delete_one(self):
        self.database.insert_one(
            collection_name=self.COLLECTION,
            document={"name": "Dave", "age": 40}
        )

        result = self.database.delete_one(
            collection_name=self.COLLECTION,
            filter_query={"name": "Dave"}
        )
        assert result.deleted_count == 1

        deleted_doc = self.database.read(
            collection_name=self.COLLECTION,
            query={"name": "Dave"}
        )
        assert deleted_doc is None
