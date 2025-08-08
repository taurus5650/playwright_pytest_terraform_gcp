import os
import textwrap
import time
from typing import Any

import certifi
import pymongo
from bson import json_util
from infra.config import get_env_config
from pymongo import errors

from utils.logger import logger


class PyMongoDB():

    def __init__(self, config: dict = None, client: pymongo.MongoClient = None):
        if config is None:
            config = get_env_config().get_dict_key('HOMEPAGE_DATABASE')
        self._config = config
        self._client = client or self.connect()
        self._db = self._client[self._config['DATABASE']]

    def remove_empty_values(self, condition: dict) -> dict:
        result = {}

        for key, value in condition.items():
            if isinstance(value, dict):  # If value = dict = nested
                cleaned_value = self.remove_empty_values(condition=value)
                if cleaned_value:
                    result[key] = cleaned_value
            elif value is not None and value != "":
                result[key] = value

        return result

    def connect(
            self, max_pool_size: int = 50, min_pool_size: int = 10, max_idle_time_ms: int = 30000,
            server_selection_timeout_ms: int = 5000):
        try:
            c = self._config
            connection_str = (
                f"mongodb+srv://{c['USER']}:{c['PASSWORD']}@{c['HOST']}/{c['DATABASE']}"
                f"?retryWrites=true&w=majority"
            )
            self._client = pymongo.MongoClient(
                connection_str, tlsCAFile=certifi.where(),
                maxPoolSize=max_pool_size,
                minPoolSize=min_pool_size,
                maxIdleTimeMS=max_idle_time_ms,
                serverSelectionTimeoutMS=server_selection_timeout_ms
            )
            self._db = self._client[self._config['DATABASE']]
            self._client.admin.command('ping')  # Testing client connection
            logger.info('MongoDB connection established successfully')
        except pymongo.errors.ConnectionFailure as e:
            logger.error(f'MongoDB ConnectionFailure: {e}"')
            self._client = None
            self._db = None
            raise
        except Exception as e:
            logger.error(f'MongoDB Exception: {e}')
            self._client = None
            self._db = None
            raise

    def get_collection(self, collection_name: str):
        return self._db[collection_name]

    def read(
            self, collection_name: str, query: dict = None, projection: dict = None,
            limit: int = 100, batch_size: int = 50,
            fetchall: bool = False, order_by: list = None):
        """
        Args:
            projection (dict, optional): Specifies which fields to include or exclude in the result.
            limit (int, optional): Maximum number of documents to return. Defaults to 100.
            batch_size (int, optional): Number of documents returned per batch by the cursor. Defaults to 50.
            fetchall (bool, required): RECOMMEND THAT USE FALSE,do avoid performance LONG QUERY issue.
        """
        query = query or {}

        start_time = time.time()

        try:
            collection = self.get_collection(collection_name)

            if not fetchall:
                sort_option = order_by if order_by else None
                res = collection.find_one(query, projection, sort=sort_option)
            else:
                cursor = collection.find(
                    query, projection=projection, batch_size=batch_size)
                if order_by:
                    cursor = cursor.sort(order_by)
                # If fetchall = True, then use limit
                res = list(cursor.limit(limit))

            duration = time.time() - start_time

            self._debug_print(
                collection_name=collection_name,
                query=query,
                result=res,
                args={
                    "operation": "find",
                    "fetchall": fetchall,
                    "order_by": order_by,
                    "limit": limit if fetchall else 1,
                    "projection": projection,
                    "duration": f"{duration:.3f}s"
                }
            )
            return res
        except pymongo.errors.PyMongoError as e:
            raise Exception(f'MongoDB PyMongoError: {e}')
        except Exception as e:
            raise Exception(f'MongoDB Exception: {e}')

    def insert_one(self, collection_name: str, document: dict):
        start_time = time.time()
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            duration = time.time() - start_time

            self._debug_print(
                collection_name=collection_name,
                query=document,
                result={"inserted_id": str(result.inserted_id)},
                args={
                    "operation": "insertOne",
                    "duration": f"{duration:.3f}s"
                }
            )
            return result
        except Exception as e:
            raise Exception(f'MongoDB Exception: {e}"')

    def update_one(
            self, collection_name: str, filter_query: dict, update_data: dict):
        start_time = time.time()
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_one(filter_query, update_data)
            duration = time.time() - start_time

            self._debug_print(
                collection_name=collection_name,
                query=filter_query,
                result={
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count
                },
                args={
                    "operation": "updateOne",
                    "update": update_data,
                    "duration": f"{duration:.3f}s"
                }
            )
            return result
        except Exception as e:
            raise Exception(f'MongoDB Exception: {e}')

    def delete_one(self, collection_name: str, filter_query: dict):
        start_time = time.time()
        try:
            collection = self.get_collection(collection_name)
            result = collection.delete_one(filter_query)
            duration = time.time() - start_time

            self._debug_print(
                collection_name=collection_name,
                query=filter_query,
                result={
                    "deleted_count": result.deleted_count
                },
                args={
                    "operation": "deleteOne",
                    "duration": f"{duration:.3f}s"
                }
            )
            return result
        except Exception as e:
            raise Exception(f'MongoDB Exception: {e}')

    def close(self):
        if self._client:
            self._client.close()
            logger.info('MongoDB connection closed"')

    def _debug_print(
            self, collection_name: str, query: Any, result: Any, args: dict = None):

        if os.getenv('debug-print', '1').lower() not in ['1', 'true']:
            return

        operation = args.get('operation') if args else "find"
        database_name = getattr(self, '_config', {}).get('DATABASE')

        if operation in ['find', 'findOne']:
            simulated_cmd = f"use {database_name};\n"
            simulated_cmd += f"db.{collection_name}.find("
            simulated_cmd += json_util.dumps(query, ensure_ascii=False)

            if args and args.get('projection'):
                simulated_cmd += f", {json_util.dumps(args['projection'], ensure_ascii=False)}"

            simulated_cmd += ")"

            if args.get('order_by'):
                simulated_cmd += f".sort({json_util.dumps(args['order_by'], ensure_ascii=False)})"
            if args.get('limit') and args['limit'] > 0:
                simulated_cmd += f".limit({args['limit']})"

            simulated_cmd += ";"

        elif operation == "insertOne":
            simulated_cmd = f"use {database_name};\n"
            simulated_cmd += f"db.{collection_name}.insertOne({json_util.dumps(query, ensure_ascii=False)});"

        elif operation == "updateOne":
            update = args.get('update', {})
            simulated_cmd = f"use {database_name};\n"
            simulated_cmd += f"db.{collection_name}.updateOne({json_util.dumps(query, ensure_ascii=False)}, {json_util.dumps(update, ensure_ascii=False)});"

        elif operation == "deleteOne":
            simulated_cmd = f"use {database_name};\n"
            simulated_cmd += f"db.{collection_name}.deleteOne({json_util.dumps(query, ensure_ascii=False)});"

        else:
            simulated_cmd = f"// Unsupported operation: {operation}"

        logger.info(textwrap.dedent(
            """
            --------------------------------
            Debug Print
            --------------------------------
            ► Collection: {collection_name}
            ► Shell Command:
            {mongo_cmd}
            ► Args:
            {args}
            ► Result:
            {result}
            --------------------------------
            """
        ).format(
            collection_name=collection_name,
            mongo_cmd=simulated_cmd,
            args=args,
            result=json_util.dumps(result, ensure_ascii=False)
        ))
