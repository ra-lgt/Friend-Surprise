import pymongo
from Configuration import Config
import requests
from bson import ObjectId



class FriendAPI:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        
        
    def send_friend_notification(self,reciever_user,sender_data):
        db = self.mongo_conn["User-Notifications"]
        collection=db[reciever_user['email']]
        
        payload={
            'sender_email':sender_data['email'],
            'sender_username':sender_data['username'],
            'sender_profile_pic':sender_data['profile_pic'],
            'notification_type':"friend_request"
            
        }
        try:
            collection.insert_one(payload)   #comment here for testing
            return True
        except Exception as e:
            return False
    
    def get_friend_notification(self,email):
        db=self.mongo_conn['User-Notifications']
        collection=db[email]
        
        cursor = collection.find({})
        user_notifcations={}
        user_notifcations['_id']=list()
        for doc in cursor:
            for key,value in doc.items():
                if key not in user_notifcations:
                    user_notifcations[key]=list()
                user_notifcations[key].append(value)
        return user_notifcations
    
    def remove_notification(self,email,id):
        db=self.mongo_conn['User-Notifications']
        collection=db[email]
        
        try:
            collection.delete_one({"_id": ObjectId(id)})
            print("Deleted")
            return True
        
        except:
            return False        
    
    def add_friend(self,sender_email,accepter_email,id):
        db=self.mongo_conn['User-FriendDB']
        collection_sender=db[sender_email]
        
        payload_sender={
            'friend_email':accepter_email
        }
        collection_sender.insert_one(payload_sender)
        
        collection_reciever=db[accepter_email]
        payload_accepter={
            'friend_email':sender_email
        }
        collection_reciever.insert_one(payload_accepter)
        
        return self.remove_notification(accepter_email,id)
        
        
        
                
                
        
    