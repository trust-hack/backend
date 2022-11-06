from pymongo import MongoClient
from bson import json_util
import json 

class Database:
    def __init__(self, conn_args, dbname):
        self.driver = MongoClient(conn_args)[dbname]

    def ping(self):
        return self.driver.command("ping")

    def login_check(self, login):
        return json.loads(
            json_util.dumps(
                self.driver.users.find_one({"login": login})
            )
        )

    def sign_up(self, user):
         return json.loads(
            json_util.dumps(
                self.driver.users.insert_one(user)
            )
        )
    
    def data_put(self, data):
        return json.loads(
                json_util.dumps(
                    self.driver.data.insert_many(data)
                )
        )
    
    def data_get(self, filt):
        return json.loads(
                json_util.dumps(
                    self.driver.data.find({"Наименование округа":filt})
                )
        )