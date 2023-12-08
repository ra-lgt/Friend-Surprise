import pymongo
from Configuration import Config


class DataAPI:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        
    def get_all_user_data(self):
        
        db = self.mongo_conn["User-Data"]
        collection=db['user_details']
        
        cursor = collection.find({})
        
        user_all_data={}
        
        #have to check whether the user is already a friend or not
        
        for doc in cursor:
            for key,value in doc.items():
                if key not in user_all_data:
                    user_all_data[key]=list()
                user_all_data[key].append(value)
                
        del user_all_data['_id']
        return user_all_data
    
    def get_data_of_specific_user(self,email):
        db = self.mongo_conn["User-Data"]
        collection=db['user_details']
        
        cursor = collection.find({"email":email})
        
        for doc in cursor:
            print(doc)
        
        return 1
        
        