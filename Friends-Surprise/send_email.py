from flask import Flask,render_template,url_for
from jinja2 import Environment,FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class send_email:
        
	def send_email_friends(participants_data):
		surprise_algorithm={}
		index=0
		
		for key,value in participants_data.items():
			
			if(len(value)>0):
				for i in range(len(value)):
					surprise_algorithm[index]={}
					surprise_algorithm[index][value[i]['email']]=list()
					
					if(i<len(value)-1):

						surprise_algorithm[index][value[i]['email']].append(value[i+1])
					else:
						surprise_algorithm[index][value[i]['email']].append(value[0])

					index+=1
		
		
						
						
					
					
					
		messages='''
		Subject: 🎉 Jolly Jot - Spread the Joy! 🎁

		Hi [Friend's Name],

		Hope this email finds you well and full of excitement! As part of our "Randomly Surprised" game, it's your turn to spread some joy and surprise a friend. Drumroll, please...

		**Your Surprise Assignment:** [Friend's Name]

		That's right! You've been chosen to surprise [Friend's Name] with a delightful gesture. Whether it's a thoughtful message, a small gift, or a fun activity, the choice is yours! The beauty of it all is the element of surprise.

		Remember, the surprise is meant to be a joyful mystery, so no need to spill the beans beforehand. Keep it hush-hush until the big reveal.

		Feel free to get creative and make it a moment to remember. The aim is to bring smiles and excitement to our little circle of friends.

		**Important Details:**
		- **Recipient:** [Friend's Name]
		- **Deadline:** [Specify a date, if desired, or leave it open-ended for an extra surprise factor]
		- **Have Fun:** The most crucial part! Enjoy the process and the anticipation.

		Let's keep the surprise spirit alive! Looking forward to hearing all about the wonderful surprises that unfold.

		Happy surprising!

		JoY Jot'''

		for key,value in surprise_algorithm.items():
			for sender_email,reciever_data in value.items():
				env = Environment(loader=FileSystemLoader('./templates'))
				template_vars = {'sender_email': sender_email, 'reciever_data': reciever_data,'message':messages}
				template = env.get_template('email-friends.html')
				output_html = template.render(template_vars)
				message=MIMEMultipart('alternative')
				message['subject']="Jolly Jot - Spread the Joy!"
				message["from"]="skillstormofficial01@gmail.com"
				message["to"]=sender_email
				html_mail=MIMEText(output_html,'html')
				message.attach(html_mail)
				server=smtplib.SMTP_SSL("smtp.gmail.com",465)
				server.login("skillstormofficial01@gmail.com","wgrrwnsolhyfiyrg")
				server.sendmail("skillstormofficial01@gmail.com",sender_email,message.as_string())


	def send_otp(self,username,email,OTP):
		messages='''Welcome to Skill-Storm!<br>

                          

Hello,

Your OTP for verification is: {}<br>

Please enter this OTP on the verification page to complete the process. This OTP is valid for a limited time.

If you didn't request this OTP, please ignore this message.<br>

Thank you,
Skill-Storm
'''.format(OTP)

		env = Environment(loader=FileSystemLoader('./templates'))
		template_vars = {'username': username, 'email': email,'message':messages}
		template = env.get_template('email.html')
		output_html = template.render(template_vars)
		message=MIMEMultipart('alternative')
		message['subject']="OTP Verification: Your One-Time Password"
		message["from"]="skillstormofficial01@gmail.com"
		message["to"]=email

		html_mail=MIMEText(output_html,'html')
		message.attach(html_mail)
		server=smtplib.SMTP_SSL("smtp.gmail.com",465)
		server.login("skillstormofficial01@gmail.com","wgrrwnsolhyfiyrg")
		server.sendmail("skillstormofficial01@gmail.com",email,message.as_string())