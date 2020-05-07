import pymongo


class Database(object):
    uri = "mongodb://127.0.0.1:27017"
    database = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.uri)
        Database.database = client['dealpro']

    @staticmethod
    def insert(collection, data):
        Database.database[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.database[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.database[collection].find_one(query)

    @staticmethod
    def find_distinct(collection, query, distinct):
        return Database.database[collection].find(query).distinct(distinct)

    @staticmethod
    def update_one(collection, query, new):
        Database.database[collection].update_one(query, {"$set": new})
