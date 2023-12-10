from flask import Flask,render_template,request,session,redirect,url_for,make_response,jsonify,send_file
import json
from Configuration import Config
from send_email import send_email
import random
from UserDataCollectionAPI import DataAPI
from flask_caching import Cache
from datetime import datetime
from FriendAPI import FriendAPI
from Event import Event

app = Flask(__name__)
config=Config()
firebase_db=config.Setup_auth()
mail=send_email()
app.secret_key = 'Friend-surprise'
mongo_client=config.create_mong_conn()
user_dataAPI=DataAPI()
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
friend=FriendAPI()
event=Event()


@app.route('/terms')
def terms():
    return "hi"
#===========================================Helping Fuctions
def generate_otp():
    sequence_length = 5
    min_value = 10 ** (sequence_length - 1)  # Smallest 5-digit number (10000)
    max_value = (10 ** sequence_length) - 1  # Largest 5-digit number (99999)
    random_number = random.randint(min_value, max_value)
    return random_number

def check_email_exists(email):
    try:
        users = firebase_db.get_user_by_email(email)
        return True
    except Exception as e:
        return False
#==========================================================Helping Funstions

#success Register
@app.route('/sucess')
def sucess():
    return render_template('success.html',data=request.args.get('data'))
    

@app.route('/sucess_register')
def sucess_register():
    return render_template('success.html',data="THANKS FOR REGISTERING")

@app.route('/error')
def error():
    data = request.args.get('data')
    reason = request.args.get('reason')
    return render_template('error.html',data={"data":data,"reason":reason})
    

#check for email exists and returns 404
@app.route('/email_exists')
def email_exists():
    return render_template('error.html',data={"reason":"Email Already Exists","data":"Try to login using valid credentials"})

#sends otp to email
@app.route('/send_otp',methods=['GET','POST'])
def send_otp():
    response_data = {'message': 'Signup successful','email_exists':False}
    print("helloo world")

    data=request.get_json()
    flag=check_email_exists(data['email'])

    if(flag==True):
        response_data['email_exists']=True
        return jsonify(response_data),404

    session['username']=data['username'].strip()
    session['email']=data['email'].strip()
    session['phone']=data['phone']
    

    if(data['password']==data['confirm_password']):

        session['password']=data['password']
        get_otp=generate_otp()
        response_data['otp']=str(get_otp)

        mail.send_otp(session['username'],session['email'],get_otp)

        return jsonify(response_data), 200

    response_data['message']='FAIL'

    return jsonify(response_data),404

#pushes data into firebase and mongo db
@app.route('/signup',methods=['GET','POST'])
def signup():

    
    database=config.Setup_DataBase()

    friend_referal_id=session.get('friends_referal_id')

    data={
        'username':session.get('username'),
        'email':session.get('email'),
        'phone':session.get('phone'),
        'password':session.get('password'),
        
        
        }

    db=mongo_client['User-Data']
    collection=db['user_details']
    current_date = datetime.now()

    collection.insert_one({
            'username':data['username'],
            'email':data['email'],
            'phone':data['phone'],
            'password':data['password'],
            'Age':"-1",
            'Address':"Not Set",
            'About':"Not Set",
            'first_name':"Not Set",
            'last_name':"Not Set",
            'City':"Not Set",
            'Country':"Not Set",
            'Postal_Code':"-1",
            'Joined_date':current_date.strftime("%Y-%m-%d")
            })
    
    firebase_db.create_user_with_email_and_password(data['email'],data['password'])
    


    session['username']=''
    session['email']=''
    session['phone']=''
    session['password']=''


    response_data = {'message': 'Signup successful'}

    return jsonify(response_data), 200 

#signup page rendering
@app.route('/signup_login')
def signup_login():
    return render_template('signup_login.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        email=request.form['loginemail']
        password=request.form['loginPassword']
    
    try:
        userauth=firebase_db.sign_in_with_email_and_password(email,password)
        session['email']=email
        session['username']=user_dataAPI.get_data_of_specific_user(email)['username']
    except:
        error_url = url_for('error', data="Invalid login", reason="Check your credentials and try again or contact us")
        return redirect(error_url)
    
    cookie=userauth['idToken']
    session['user_id'] = cookie
    
    return redirect(url_for('Home'))

@app.route('/logout')
def logout():
    # Clear the user ID from the session
    session.pop('user_id', None)
    session.clear()
    cache.clear()
    return redirect(url_for('Home'))

@app.route('/view_user_friends',methods=['POST','GET'])
def view_user_friends():
    friend_data=None
    friend_data=cache.get('user_friend_data')
    
    if(friend_data is None):
        
        friend_data=friend.get_friends_specific_user(session['email'])
        cache.set("user_friend_data",friend_data,timeout=180*60)
        
    return render_template('user_friends.html',friend_data=friend_data,count=len(friend_data['_id']))


@app.route('/profile',methods=['GET','POST'])
def profile():
    user_specific_data=None
    user_specific_data=cache.get('profile_data')
    
    user_specific_event=None
    user_specific_event=cache.get('event_data')
    
    friend_data=None
    friend_data=cache.get('user_friend_data')
    
    if(friend_data is None):
        
        friend_data=friend.get_friends_specific_user(session['email'])
        cache.set("user_friend_data",friend_data,timeout=180*60)
    
    
    if(user_specific_event is None):
        user_specific_event=event.get_event_for_user(session['email'])
        cache.set('event_data',user_specific_event,timeout=180*60)
    
    if(user_specific_data is None):
        user_specific_data=user_dataAPI.get_data_of_specific_user(session['email'])
        cache.set('profile_data',user_specific_data,timeout=180*60)
    else:
        print("cache Hit")

    

    return render_template("profile.html",user_specific_data=user_specific_data,event_count=len(user_specific_event['_id']),friend_count=len(friend_data['_id']))

@app.route('/update_profile_data',methods=['POST'])
def update_profile_data():
  
    
    updated_data={}
    
    
    updated_data['first_name']=request.form['f_name']
    updated_data['last_name']=request.form['l_name']
    updated_data['phone']=request.form['phone']
    updated_data['Age']=request.form['age']
    updated_data['Address']=request.form['address']
    updated_data['City']=request.form['city']
    updated_data['Country']=request.form['country']
    updated_data['Postal_Code']=request.form['postal']
    updated_data['About']=request.form['about']
    
    return_code=user_dataAPI.update_profile(updated_data,session['email'])
    
    if(return_code==True):
        
        cache.clear()
        return redirect(url_for('profile'))
    
    else:
        return redirect(url_for('error',data="Couldn't Update",reason="Try to update again you should have strong internet"))

@app.route('/create_event_data',methods=['POST','GET'])
def create_event_data():
    event_data=request.get_json()
    return_code=event.create_event(event_data,session['email'])
    
    if(return_code==True):
        return jsonify({"status":200}),200
    else:
        return jsonify({"status":404}),404
    
@app.route('/create_event')
def create_event():
    friend_data=None
    friend_data=cache.get('user_friend_data')
    if(friend_data is None):
        
        friend_data=friend.get_friends_specific_user(session['email'])
        cache.set("user_friend_data",friend_data,timeout=180*60)
        
    return render_template('create.html',friend_data=friend_data,count=len(friend_data['_id']))

@app.route('/notification')
def notification():
    user_notifications=None
    user_notifications=cache.get("notifications")
    if(user_notifications is None):
        user_notifications=friend.get_friend_notification(session['email'])
        cache.set("notifications",user_notifications,timeout=180*60)
    
    
    return render_template('message.html',notifications=user_notifications,count=len(user_notifications['_id']))

@app.route('/accepted_request',methods=['POST','GET'])
def accepted_request():
    sender_data=request.get_json()
    
    
    return_code=friend.add_friend(sender_data,session['email'],session['username'])
    
    if(return_code==True):
        cache.clear()
        return jsonify({'status':200}),200
    else:
        return jsonify({"status":404}),404
        
    
@app.route('/send_friend_request',methods=['POST','GET'])
def send_friend_request():
    
    friend_request=request.get_json()
    user_specific_data=None
    user_specific_data=cache.get('profile_data')
    
    if(user_specific_data is None):
        user_specific_data=user_dataAPI.get_data_of_specific_user(session['email'])
        cache.set('profile_data',user_specific_data,timeout=180*60)
    else:
        print("cache Hit")
    
    return_code=friend.send_friend_notification(friend_request,user_specific_data)
    
    if(return_code==True):
        message={'message':'successfully sent','status':200}
        return jsonify(message),200
    
    return jsonify({'message':'error in request','status':404}),404
    


@app.route('/save_profile_pic',methods=['POST'])
def save_profile_pic():
    
    if 'file' not in request.files:
        print("file not found")
    file = request.files['file']

    return_code=user_dataAPI.save_profile(file,cache.get('profile_data')['username'])
    
    if(return_code==True):
        result = {'message': 'Image uploaded successfully'}
        return jsonify(result)
    else:
        result = {'error': 'Unexpected error occured'}
        return jsonify(result)
        

@app.route('/find_friends')
def find_friends():
    all_user_data=None
    all_user_data = cache.get('cached_all_user_data')
    print("cache data",all_user_data)
    
    if(all_user_data is None):
        
        all_user_data=user_dataAPI.get_all_user_data(session['email'])
        
        cache.set('cached_all_user_data', all_user_data, timeout=180 * 60)
    else:
        print("Cache hit")
    
    country=[]
        
    for i in all_user_data['Country']:
        if(i not in country and i!="Not Set"):
            country.append(i)
    
    if not all_user_data:
        count=0
    else:
        count=len(all_user_data['username'])
    return render_template('find_friends.html',all_user_data=all_user_data,count=count,country=country)

@app.route('/')
def Home():
    session_bool=False
    
    if('user_id' in session):
        session_bool=True
    
    
    return render_template('index.html',session_bool=session_bool)

if __name__ == '__main__':
    app.run(debug=True)
