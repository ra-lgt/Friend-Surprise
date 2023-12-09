import pyrebase
import pymongo


class Config:
	def __init__(self):
		self.firebaseConfig={
  			'apiKey': "AIzaSyBLvQjHofPRr9fsAp9CPksdLA_gJ9UP31Q",
  			'authDomain': "friend-surprise.firebaseapp.com",
  			'projectId': "friend-surprise",
  			'storageBucket': "friend-surprise.appspot.com",
  			'messagingSenderId': "1059250399150",
  			'appId': "1:1059250399150:web:7dc74994ea4e7a5462ca3f",
  			'measurementId': "G-JY8TDPPH1H",
  			"databaseURL":"https://friend-surprise-default-rtdb.firebaseio.com/"}
		self.firebase=pyrebase.initialize_app(self.firebaseConfig)
		self.client = pymongo.MongoClient("mongodb+srv://raviajay9344:RIa3f6h32MeSg7MV@friends-surprise-db.dvda3zg.mongodb.net/")

	def Setup_auth(self):
		return self.firebase.auth()

	def Setup_DataBase(self):
		return self.firebase.database()

	def create_mong_conn(self):
		return self.client

	def Setup_Storage(self):
		return self.firebase.storage()


