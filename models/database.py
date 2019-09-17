import pymongo
import gridfs


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    FS = None

    @staticmethod
    def initialize(datab):
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[datab]
        FS = gridfs.GridFS(Database.DATABASE)

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return list(Database.DATABASE[collection].find(query))

    @staticmethod
    def count(collection, query={}):
        return Database.DATABASE[collection].count_documents(query)

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].delete_one(query).deleted_count

    @staticmethod
    def delete_all(collection, query={}):
        return Database.DATABASE[collection].delete_many(query).deleted_count

    @staticmethod
    def update(collection, query, update_query):
        return Database.DATABASE[collection].update(query,
                                                    {"$set": update_query})

    @staticmethod
    def updateMany(collection, query, update_query):
        if update_query.get('$inc'):
            return Database.DATABASE[collection].update(query, update_query)

        return Database.DATABASE[collection].update_many(query,
                                                         {"$set": update_query})

    @staticmethod
    def saveFile(binaryObj):
        """
        Takes binaryObj and stores it in MongoDB using GridFS 

        Returns ObjectID of the stored file
        """
        return FS.put(binaryObj)

    @staticmethod
    def loadFile(_id):
        """
        Takes ObjectID and retrieves it from MongoDB using GridFS 

        Returns stored file
        """
        out = FS.get(_id)
        return {'file': out,
                'created_at': out.upload_date}

    @staticmethod
    def created_at(_id):
        return _id.generation_time
