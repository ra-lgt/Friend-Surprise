import pymongo
from Configuration import Config
import requests
from bson import ObjectId
from UserDataCollectionAPI import DataAPI



class FriendAPI:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        self.dataapi=DataAPI()
        
        
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
    
    def add_friend(self,sender_data,accepter_email,accepter_username):
        db=self.mongo_conn['User-FriendDB']
        collection_sender=db[sender_data['sender_email']]
        
        payload_sender={
            'friend_email':accepter_email,
            'friend_username':accepter_username,
            'friend_profile':self.dataapi.get_profile_pic(accepter_username)
        }
        collection_sender.insert_one(payload_sender)
        
        collection_reciever=db[accepter_email]
        payload_accepter={
            'friend_email':sender_data['sender_email'],
            'friend_username':sender_data['sender_username'],
            'friend_profile_pic':sender_data['sender_profile_pic']
        }
        collection_reciever.insert_one(payload_accepter)
        
        return self.remove_notification(accepter_email,sender_data['id'])
    
    def get_friends_specific_user(self,email):
        db=self.mongo_conn['User-FriendDB']
        collection=db[email]
        
        cursor=collection.find({})
        
        friend_data={}
        friend_data['_id']=list()
        
        for doc in cursor:
            for key,value in doc.items():
                if key not in friend_data:
                    friend_data[key]=list()
                friend_data[key].append(value)
        
        return friend_data
        
        
        
        
        
                
                
        
    