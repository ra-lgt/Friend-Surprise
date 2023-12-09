import pymongo
from Configuration import Config
import requests



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
            
        }
        try:
            collection.insert_one(payload)   #comment here for testing
            return True
        except Exception as e:
            return False
        
    