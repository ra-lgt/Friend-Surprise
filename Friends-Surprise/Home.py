from flask import Flask,render_template,request,session,redirect,url_for,make_response,jsonify,send_file
import json
from Configuration import Config
from send_email import send_email
import random

app = Flask(__name__)
config=Config()
firebase_db=config.Setup_auth()
mail=send_email()
app.secret_key = 'Friend-surprise'
mongo_client=config.create_mong_conn()


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

    collection.insert_one({
            'username':data['username'],
            'email':data['email'],
            'phone':data['phone'],
            'password':data['password']
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
    return redirect(url_for('Home'))

@app.route('/')
def Home():
    session_bool=False
    
    if('user_id' in session):
        session_bool=True
    
    
    return render_template('index.html',session_bool=session_bool)

if __name__ == '__main__':
    app.run(debug=True)
