import pymongo
from Configuration import Config
import requests


class Event:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        
    def create_event(self,event_data,host_email):
        db=self.mongo_conn['Event-Date']
        collection=db[host_email]
        
        try:
            collection.insert_one(event_data)
            return True
        except:
            return False
    
    def get_event_for_user(self,email):
        db=self.mongo_conn['Event-Date']
        collection=db[email]
        
        cursor=collection.find({})
        user_event={}
        user_event['_id']=list()
        
        for doc in cursor:
            for key,value in doc.items():
                if key not in user_event:
                    user_event[key]=list()
                user_event[key].append(value)
        return user_event
                
        