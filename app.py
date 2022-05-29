from tkinter import Image
from flask import Flask, render_template, request,redirect,url_for
import mysql.connector
import os
from flask_mail import Mail,Message
from numpy import imag
import pandas as pd

# from jinja2 import url_for
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'projectsupervisor124@gmail.com'
app.config['MAIL_PASSWORD'] = '10162738'
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/", methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        username = request.form.get('username')
        password = request.form.get('password')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Username, Password FROM admin")

        myresult = mycursor.fetchall()

        for x in myresult:
            if(x[0] == username and x[1] == password):
                return render_template("/required.html")

        print(username)
        mycursor.close()
        mydb.close()

    return render_template("admin.html")


@app.route("/required", methods=['GET', 'POST'])
def required_page():
    return render_template("required.html")


@app.route("/runcode/", methods=['GET', 'POST'])
def run_code():

    os.system("start python MaskDetection.py")
    print("Called")
    return "Press Back button to move to dashboard"

@app.route("/sendemail/", methods=['GET', 'POST'])
def send_email():

    with open('FinalLog.csv','r') as f:
        # myDataList = f.readlines()
        emailList = []
        
        for line in f:
            entry = line.split(',')
            email=entry[2]
            
            if email not in emailList and email!='' and email!='email' and email!='unnamed' and email!='0':
                emailList.append(entry[1])
                time = entry[3]
                date = entry[4]
                msg=Message('Notification',sender ='projectsupervisor124@gmail.com', recipients = [email], body='Detected at : '+time+' on Date : '+date)
                path = r'.\Detected/'+email.lower()+'.jpeg'
                with app.open_resource(path) as fp:  
                    msg.attach(path,"image/jpeg",fp.read())
                    mail.send(msg)
    
    data=pd.read_csv('Log.csv')

    names = []
    for x in data.columns:
        if x=='email' or x=='time' or x=='date' or x==' ':
            names.append(x)
    print(names)
    df_b = pd.DataFrame(columns=names)
    print(df_b)
    df_b.to_csv('Log.csv')
    
    data=pd.read_csv('FinalLog.csv')

    names = []
    for x in data.columns:
        if x=='email' or x=='time' or x=='date' or x==' ':
            names.append(x)
    print(names)
    df_b = pd.DataFrame(columns=names)
    print(df_b)
    df_b.to_csv('FinalLog.csv')
                
    print(emailList)
    # return render_template(url_for('http://127.0.0.1:5000/required.html'))
    return "Press Back button to move to dashboard"
    # return render_template("required.html")


if __name__ == "__main__":
    app.run(debug=True)
