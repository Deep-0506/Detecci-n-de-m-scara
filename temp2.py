#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import face_recognition
from datetime import datetime


# In[3]:


# Mask Detector model


# In[3]:


def detectMask(frame, faceNet, maskNet):

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)

    faces = []
    locs = []
    preds = []


    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces.append(face)
            locs.append((startX, startY, endX, endY))


    if len(faces) > 0:

        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    return (locs, preds)


# In[4]:


pPath = r"face_detector\deploy.prototxt"
wPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceDetect = cv2.dnn.readNet(pPath, wPath)


# In[5]:


maskDetect = load_model("maskdetector.model")


# In[7]:


# Fetch Database images 


# In[6]:


from sqlalchemy import create_engine
engine = create_engine("mysql://root:@localhost/project",echo = True)
conn = engine.connect()


# In[7]:


my_cursor=conn.execute("SELECT * FROM  register")
my_result=my_cursor.fetchall()
for row  in my_result:
    print(row)
    fob=open(r'C:\Users\Dell\Desktop\Jainam docs\Deteccion de mascara\Admin\Database Images/'+ str(row[0])+'.jpeg','wb')
    fob=fob.write(row[3])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[10]:


# Face Recognition


# In[8]:


path=r"C:\Users\Dell\Desktop\Jainam docs\Deteccion de mascara\Admin\Database Images"
personimages=[]
emails=[]
imagelist=os.listdir(path)
print(imagelist)


# In[8]:


for current_img in imagelist:
    current=cv2.imread(f'{path}/{current_img}')
#     print(current)
    personimages.append(current)
    name=os.path.splitext(current_img)
#     print(name[0])
    emails.append(name[0])

print(emails)


# In[9]:


def faceEncodings(images):
    encodeList=[]
    count=0
    for img in images:
        print("Generating Encodings for Image No : ",count)
        count=count+1
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# In[13]:


def addLog(email):

    with open('Log.csv','r+') as f:
        myDataList = f.readlines()
        emailList = []

        for line in f:
            entry = line.split(',')
            emailList.append(entry[0])
        temp=""
        if email not in emailList:
            time_now = datetime.now()
            time= time_now.strftime('%H:%M:%S')
            date= time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{temp},{email},{time},{date}')
        


# In[1]:


import matplotlib.pyplot as plt
import matplotlib.image as i
from PIL import Image as im
import pandas as pd


# In[14]:


enc=faceEncodings(personimages)
print("All Encodings completed : ")

capture=cv2.VideoCapture(0)
while True:
    flag,frame=capture.read()
    if flag:
        frame=imutils.resize(frame,width=600)
        (locs, preds) = detectMask(frame, faceDetect, maskDetect)
        for (box, pred) in zip(locs, preds):
    
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            
            if mask > withoutMask:
                label = "Mask"
            else:
                label="No Mask"
                
            if label == "Mask":
                color = (0, 255, 0) 
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                
            else :
                color = (0, 0, 255)
                faces=cv2.resize(frame,(0,0),None,0.25,0.25)
                faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
#                 plt.imshow(faces)
                facesCurrentFrame = face_recognition.face_locations(faces)
                encodesCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)
#                 print(faces)
                for encodeFace,faceLoc in zip(encodesCurrentFrame,facesCurrentFrame) : 

                    matches = face_recognition.compare_faces(enc,encodeFace)
                    faceDis = face_recognition.face_distance(enc,encodeFace)

                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex] : 
                        name=emails[matchIndex].upper()
                        print(name)
                        data = im.fromarray(faces)
                        data.save(r'C:\Users\Dell\Desktop\Jainam docs\Deteccion de mascara\Admin\Detected/'+name.lower()+'.jpeg')
#                         fob=open(r'C:\Users\Dell\Desktop\Jainam docs\Deteccion de mascara\Database Images/'+name+'.jpeg','wb')
#                         fob=fob.write(row[3])
#                         mail=conn.execute("INSERT INTO  images(email,img) VALUES (%s,%s)",name,faces.read())
#                         print("Row Added  = ",mail.rowcount)
                        text=label+" "+name
                        cv2.putText(frame, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                        addLog(name)            
            
        cv2.imshow("Live Video",frame)
        if cv2.waitKey(2) == 27:
            break
else:
    
    data=pd.read_csv('Log.csv')
    data = data.sort_values(by = ['date', 'time'], ascending = [False, False])
    data.drop_duplicates(subset="email",inplace=True)
    # data
    data.to_csv('FinalLog.csv')
capture.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:




