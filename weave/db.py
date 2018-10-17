import os
import psycopg2
import operator
import hashlib
from collections import Counter
import json

# CREATE TABLE weave_data (
#     user_id VARCHAR(255) NOT NULL PRIMARY KEY,
#     user_data JSON
# );


class DBConnection:
    def __init__(self):
        print("connecting to db")
        self.conn = psycopg2.connect(
            host=os.environ['db_host'], dbname=os.environ['db_dbname'], user=os.environ['db_user'], password=os.environ['db_password'])
        self.cur = self.conn.cursor()
        print("connected to db")

    def get_alarm(self):
        print("getting user data")
        user_id = 'alarm'
        if self.check_exist(user_id):
            query = "SELECT user_data FROM weave_data WHERE user_id = '{}';".format(
                user_id)
            self.cur.execute(query)
            result = self.cur.fetchone()[0]
            print("got user data")
        else:
            result = {
                'switch': 0
            }
            self.insert(user_id, result)
        return result

    def insert(self, user_id, json_data):
        query = "INSERT INTO weave_data VALUES (%s, %s);"
        data = (user_id, json.dumps(json_data))
        self.cur.execute(query, data)
        self.conn.commit()

    def empty_json_data(self):
        data = {
            "lists": {
                "current": {
                    "items": [],
                    "subtotal": 0,
                    "discount": 0,
                    "total": 0
                }
            },
            "shopping": {
                "items": [],
                "subtotal": 0,
                "discount": 0,
                "total": 0
            }
        }
        return data

    def get(self, user_id):
        print("getting user data")
        if self.check_exist(user_id):
            query = "SELECT user_data FROM weave_data WHERE user_id = '{}';".format(
                user_id)
            self.cur.execute(query)
            result = self.cur.fetchone()[0]
            print("got user data")
        else:
            result = self.empty_json_data()
            self.insert(user_id, result)
            print("user not found, creating user")
        return result

    def update(self, user_id, json_data):
        print(json_data)
        query = "UPDATE weave_data SET user_data = %s WHERE user_id = %s;"
        data = (json.dumps(json_data), user_id)
        self.cur.execute(query, data)
        self.conn.commit()

    def update_with_item(self, user_id, item):
        json_data = self.get(user_id)
        json_data['items'].append(item)
        self.update(user_id, json_data)

    def check_exist(self, user_id):
        # Check if email exists in User Table
        query = "SELECT * FROM weave_data WHERE user_id = '{}';".format(
            user_id)
        self.cur.execute(query)
        return self.cur.rowcount
