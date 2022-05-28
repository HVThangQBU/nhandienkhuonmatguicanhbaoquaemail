import os,shutil
import cv2 as cv
import numpy as np
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import smtplib, ssl
from tkinter import*
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from faceTrain import*
import mediapipe as mp
import pyttsx3
import speech_recognition as sr

friday=pyttsx3.init()
voices = friday.getProperty('voices')
friday.setProperty('voice', voices[1].id) 
def speak(audio):
    print('F.R.I.D.A.Y: ' + audio)
    friday.say(audio)
    friday.runAndWait()
   

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

window = tk.Tk()
window.minsize(1500, 700)
window.title("Face_Recogniser")
window.configure(background ='white')
window.grid_rowconfigure(0, weight = 1)
window.grid_columnconfigure(0, weight = 1)
message = tk.Label(
    window, text ="Cảnh báo khuôn mặt lạ",
    bg ="green", fg = "white", width = 50,
    height = 3, font = ('times', 30, 'bold'))
     
message.place(x = 200, y = 20)
 
lbl = tk.Label(window, text = "Nhập mail muốn gửi cảnh báo",
width = 30, height = 2, fg ="blue",
bg = "white", font = ('times', 15, ' bold ') )
lbl.place(x = 350, y = 200)
 
txt = tk.Entry(window,
width = 30, bg ="white",
fg ="green", font = ('times', 15, ' bold '))
txt.place(x = 700, y = 215)
 
lbl2 = tk.Label(window, text ="Nhập tên khuôn mặt muốn thêm",
width = 30, fg ="blue", bg ="white",
height = 2, font =('times', 15, ' bold '))
lbl2.place(x = 350, y = 300)
 
txt2 = tk.Entry(window, width = 30,
bg ="white", fg ="green",
font = ('times', 15, ' bold ')  )
txt2.place(x = 700, y = 315)

def sendAlertEmail(i):
    email =(txt.get())
    
    fromaddr = "hoangthangd5ddt@gmail.com"
    toaddr = email

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Subject of the Mail"

    # string to store the body of the mail
    body = "Có người lạ đang sử dụng máy của bạn!!! "

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = 'Face Recognition App\imagesnotme\Frame'+str(i)+'.jpg'
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "aiompucqiimbojni")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

def sendErrorEmail():
    email =(txt.get())
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # sampe server
    sender_email = "hoangthangd5ddt@gmail.com"  # sample sender address
    receiver_email = email  # sample receiver address
    password = "pypxchtpsjfsjwlg" # sample password
    message = "Detected error with camera"
    # send email with server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
def TakeImages():       
    name =(txt2.get())
    if len(txt2.get()) == 0:
        res = "Vui lòng nhập tên" 
        message.configure(text = res)     
    # Checking if the ID is numeric and name is Alphabetical
    if(name.isalpha()):
        # cam = cv.VideoCapture(0,cv.CAP_DSHOW)
        # url = "https://192.168.31.115:8080/video"
        # cam.open(url)
        #cam amy tinh
        cam = cv.VideoCapture(0)
        sampleNum = 0
        with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
            while(True):
                # Reading the video captures by camera frame by frame
                ret, img = cam.read()
                img.flags.writeable = False
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                results = face_detection.process(img)
                    # Draw the face detection annotations on the image.
                img.flags.writeable = True
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                img_height, img_width, _ = img.shape
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                if results.detections:
                    for detection in results.detections:   
                        mp_drawing.draw_detection(img, detection)
                        x = int(min(detection.location_data.relative_bounding_box.xmin, 1) * img_width)
                        y = int(min(detection.location_data.relative_bounding_box.ymin, 1) * img_height)
                        x_max = int(min(detection.location_data.relative_bounding_box.xmin + detection.location_data.relative_bounding_box.width, 1) * img_width)
                        y_max = int(min(detection.location_data.relative_bounding_box.ymin + detection.location_data.relative_bounding_box.height, 1) * img_height)
                        faces_roi = gray[y:y_max,x:x_max]
                        if 0 in faces_roi.shape:
                            continue
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    # TrainingImage as the image needs to be trained
                    # are saved in this folder
                    cv.imwrite(
                        "Face Recognition App\images, training\me\ "+name + str(
                            sampleNum) + ".PNG", faces_roi)
                    # display the frame that has been captured
                    # and drawn rectangle around it.
                    cv.imshow('frame', img)
                # wait for 100 milliseconds
                if cv.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 60
                elif sampleNum>400:
                    break
        # releasing the resources
        cam.release()
        # closing all the windows
        cv.destroyAllWindows()
        # Displaying message for the user
        res = "Thêm khuôn mặt thành công" 

        message.configure(text = res)
    else:
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text = res)


def remove():
    folder = "Face Recognition App/images, training/me"
    for the_file in os.listdir(folder):
        #file_path = os.path.join(folder, the_file)
        shutil.rmtree(folder)
        os.mkdir(folder)

def detect():
    res = "Vui lòng nhập Email"
    if len(txt.get()) == 0:
        message.configure(text = res)   
    
    i = 0
    # turn on camera
    # vid = cv.VideoCapture(0,cv.CAP_DSHOW)
    # url = "https://192.168.31.115:8080/video"
    # vid.open(url)
    vid = cv.VideoCapture(0)
    people = ["me", "not me"]
    # create face recognizer
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    # input pre-made .yml into recognizer
    face_recognizer.read('face_trained.yml')
    if not vid.isOpened():
        # send error message if camera is not opened
        sendErrorEmail()
        exit()
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        while vid.isOpened():
        
            # read image from camera
            isTrue, img = vid.read()
            if (isTrue):
                img.flags.writeable = False
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                results = face_detection.process(img)
                # Draw the face detection annotations on the image.
                img.flags.writeable = True
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                img_height, img_width, _ = img.shape
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                if results.detections:
                    for detection in results.detections:   
                        print('haha',detection)
                        mp_drawing.draw_detection(img, detection)
                        x = int(min(detection.location_data.relative_bounding_box.xmin, 1) * img_width)
                        y = int(min(detection.location_data.relative_bounding_box.ymin, 1) * img_height)
                        x_max = int(min(detection.location_data.relative_bounding_box.xmin + detection.location_data.relative_bounding_box.width, 1) * img_width)
                        y_max = int(min(detection.location_data.relative_bounding_box.ymin + detection.location_data.relative_bounding_box.height, 1) * img_height)
                        faces_roi = gray[y:y_max,x:x_max]
                        if 0 in faces_roi.shape:
                            continue
                        cv.rectangle(img, (x,y), (x_max,y_max), (0,255,0), thickness=2)
                        print(faces_roi.shape)
                        label, confidence = face_recognizer.predict(faces_roi)
                        print(confidence)
                        cv.putText(img, str(people[label]), (x_max + 10,y_max + 10), cv.FONT_HERSHEY_COMPLEX,  1, (255, 255, 255), 4, cv.LINE_AA)
                       # doan nay he thong thong minh 
                        if str(people[label]) != "me":
                            # send alert email to user if intruder is detected
                            speak("please turn off")
                            cv.imwrite('Face Recognition App\imagesnotme\Frame'+str(i)+'.jpg', img)
                            sendAlertEmail(i)
                            i += 1
                            print("da gui canh bao")
                        else:
                            continue
                    cv.imshow('Frame', img) 
                    if (cv.waitKey(10)== ord('q')):
                        break     
            # else:
            #     # send error message if image can't be read
            #     sendErrorEmail()
            #     exit()

            # pause 60 seconds
            #time.sleep(20)
        vid.release()
        cv.destroyAllWindows()
        exit()

takeImg = tk.Button(window, text ="Thêm khuôn mặt",
command = TakeImages, fg ="white", bg ="blue",
width = 20, height = 3, activebackground = "Red",
font =('times', 15, ' bold '))
takeImg.place(x = 320, y = 500)
RemoveImg = tk.Button(window, text ="Xóa khuôn mặt",
command = remove, fg ="white", bg ="blue",
width = 20, height = 3, activebackground = "Red",
font =('times', 15, ' bold '))
RemoveImg.place(x = 10, y = 500)
trainImg = tk.Button(window, text ="Huấn luyện",
command = train, fg ="white", bg ="blue",
width = 20, height = 3, activebackground = "Red",
font =('times', 15, ' bold '))
trainImg.place(x = 620, y = 500)
trackImg = tk.Button(window, text ="Bắt đầu ",
command = detect, fg ="white", bg ="blue",
width = 20, height = 3, activebackground = "Red",
font =('times', 15, ' bold '))
trackImg.place(x = 920, y = 500)
quitWindow = tk.Button(window, text ="Thoát",
command = window.quit, fg ="white", bg ="blue",
width = 20, height = 3, activebackground = "Red",
font =('times', 15, ' bold '))
quitWindow.place(x = 1220, y = 500)
  
window.mainloop()