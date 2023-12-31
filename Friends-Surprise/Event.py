import pymongo
from Configuration import Config
import requests
from datetime import datetime


class Event:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        
    def create_event(self,event_data,host_email):
        db=self.mongo_conn['Event-Date']
        collection=db[host_email]
        
        collection_curr=db['Current-Event']
        # collection_curr.create_index([("Event_Date", pymongo.ASCENDING)])
        event_data['Event_Date']=datetime.strptime(event_data['Event_Date'], "%Y-%m-%d")
        
        try:
            collection.insert_one(event_data)
            collection_curr.insert_one(event_data)
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
    
    
    def check_for_today_event(self):
        db=self.mongo_conn['Event-Date']
        collection_curr=db['Current-Event']
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        
        cursor=collection_curr.find({})
        document_count = collection_curr.count_documents({})
        
        participants_email={}
        index=0
        
        for doc in cursor:
            
            formatted_date_mongo = doc['Event_Date'].strftime("%Y-%m-%d")
            
            if(formatted_date==formatted_date_mongo):
                participants_email[index]=list()
                for email in doc['Event_Friends']:
                    participants_email[index].append(email)
                index+=1
                
        return participants_email
        
        
        
                            
                        
            
                
        