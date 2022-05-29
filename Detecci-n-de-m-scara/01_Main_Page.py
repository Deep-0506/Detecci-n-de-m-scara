from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from flask_mail import Mail,Message

from sqlalchemy import null

application = Flask(__name__)
application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'projectsupervisor124@gmail.com'
application.config['MAIL_PASSWORD'] = '10162738'
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)

with open("02_config.json","r") as d:
    parameters = json.load(d)["parameters"]

Local_Server = parameters["Local_Server"]

if(Local_Server):
    application.config["SQLALCHEMY_DATABASE_URI"] = parameters["Local_URI"]
else:
    application.config["SQLALCHEMY_DATABASE_URI"] = parameters["Prod_URI"]

database = SQLAlchemy(application)

class Contact(database.Model):

    SrNo = database.Column(database.Integer , primary_key = True)
    Name = database.Column(database.String(255) , nullable = False)
    Email = database.Column(database.String(255) , nullable = False)
    Phone_Number = database.Column(database.String(255) , nullable = False)
    Message = database.Column(database.String(255) , nullable = False)


# class Register(database.Model):

#     SrNo = database.Column(database.Integer , primary_key = True)
#     Name = database.Column(database.String(255) , nullable = False)
#     Email = database.Column(database.String(255) , nullable = False)
#     Phone_Number = database.Column(database.String(255) , nullable = False)
#     Image = database.Column(database.Text , nullable = False)


@application.route("/")
def Main_Page():

    return render_template("index.html")

@application.route("/about")
def about():

    return render_template("about.html")

@application.route("/contact" , methods = ["POST" , "GET"])
def contact():

    if(request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        message = request.form.get("message")
        em="projectsupervisor124@gmail.com"
        msg=Message('Mail from User',sender ='projectsupervisor124@gmail.com', recipients = [em], body=" "+email+" has mailed you.\n Message : "+message+" \n Name : "+name+" \n Phone Number : "+phone_number)
        mail.send(msg)
    return render_template("contact.html")

@application.route("/registration" , methods = ["POST" , "GET"])
def registration():

    if(request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        # image = request.form.get("image")
        file = request.files["image"]
        img = file.read()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO register (Email,Name,Phone_Number,Image) VALUES (%s, %s,%s,%s)"
        val = (email,name,phone_number,img)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        msg=Message('Registered',sender ='projectsupervisor124@gmail.com', recipients = [email], body='You are Successfully registered.')
        mail.send(msg)
        # mycursor = mydb.cursor()
        # Entry2 = Register(Name = name , Email = email , Phone_Number = phone_number , Image = image)
        # database.session.add(Entry2)
        # database.session.commit()

    return render_template("registration.html")

application.run(debug=True,port=5001)