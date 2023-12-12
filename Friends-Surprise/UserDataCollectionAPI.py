import pymongo
from Configuration import Config
import requests


class DataAPI:
    def __init__(self):
        self.config=Config()
        self.mongo_conn=self.config.create_mong_conn()
        self.storage=self.config.Setup_Storage()
        
    def get_all_user_data(self,email):
        from FriendAPI import FriendAPI
        friend=FriendAPI()
        friend_email=[]
        try:
            friend_email=friend.get_friends_specific_user(email)['friend_email']
        except:
            pass
        
        
        db = self.mongo_conn["User-Data"]
        collection=db['user_details']
        
        
        query = {
    "$and": [
        {"email": {"$ne": email}},
        {"email": {"$nin": friend_email}}
        
    ]
}
        
        cursor = collection.find(query)
        
        user_all_data={}
        
        #have to check whether the user is already a friend or not
        user_all_data['profile_url']=list()
        
        for doc in cursor:
            for key,value in doc.items():
                
                if key not in user_all_data:
                    user_all_data[key]=list()
                user_all_data[key].append(value)
                
                if(key=="username"):
                    
                    user_all_data['profile_url'].append(self.get_profile_pic(value))
                    
                    
        try:        
            del user_all_data['_id']
        except:
            pass
        
        return user_all_data
    def is_url_exists(self,url):
        response=requests.get(url)

        if(response.status_code==200):
            return True
        else:
            return False
    
    def get_profile_pic(self,username):		
        url=self.storage.child(username).get_url(None) or None

        if (not self.is_url_exists(url)):
            url=""
        if(url==""):
            url=self.storage.child("default_profile.jpg").get_url(None) or None
            

        return url
    
    def get_data_of_specific_user(self,email):
        db = self.mongo_conn["User-Data"]
        collection=db['user_details']
        
        cursor = collection.find({"email":email})
        
        data=None
        for doc in cursor:
            data=doc
            break
        data['profile_pic']=self.get_profile_pic(data['username'])
        
        return data
    
    def update_profile(self,updated_data,email):
        db = self.mongo_conn["User-Data"]
        collection=db['user_details']
        
        filter={"email":email}
        update={"$set":updated_data}
        
        try:
            collection.update_one(filter, update)
            return True
        except Exception as e:
            print(e)
            return False
        

    def save_profile(self,file,username):
        try:
            self.storage.child(username).put(file)
            print("hi Updated",file)
            return True
        except Exception as e:
            print(e)
            print(file)
            return  False
        
    def get_user_data_in_event(self,participants_email):
        
        participants_data={}
        index=0
        
        for key,value in participants_email.items():
            participants_data[index]=list()
            for email in value:
                participants_data[index].append(self.get_data_of_specific_user(email))
                
            index+=1
        
        return participants_data
                
                

        
        