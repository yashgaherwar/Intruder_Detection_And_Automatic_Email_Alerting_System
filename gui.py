from tkinter import *
from tkinter.font import families
import glob
import face_recognition
import cv2
import numpy as np
import jovian
import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from mysql_database import connections


def delete2():
    screen3.destroy()
    screen2.destroy()
    screen.destroy()

def delete3():
    screen4.destroy()

def delete4():
    screen5.destroy()


def login_sucess():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Success")
    screen3.geometry("400x250")
    Label(screen3, text="Login Sucess").pack()
    Button(screen3, text="OK", height='2', width="15").pack()
    screen3.destroy()
    screen2.destroy()
    screen.destroy()
    system()

def password_not_recognised():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Success")
    screen4.geometry("500x350")
    Label(screen4, text="Password or Email Error").pack()
    Button(screen4, text="OK", command=delete3).pack()

def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Success")
    screen5.geometry("500x350")
    Label(screen5, text="User Not Found").pack()
    Button(screen5, text="OK", command=delete4).pack()

def des2():
    screen2.destroy()
    screen1.destroy()

def success():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Successfully Register")
    screen2.geometry("500x350")
    Label(screen2, text="Registration Successful", fg="green", font=("calibri", 11)).pack()
    Label(screen1, text="").pack()
    Button(screen2, text="ok", bg="lightgreen", height="2", width="20", command=des2).pack()


def register_user():
    print("working")

    email_info = email.get()
    password_info = password.get()
    connection1 = connections()
    res=connection1.database_insert(email_info,password_info)
    print(res)

    file = open("Details.txt", "a")
    file.write("\n"+email_info + "\n")
    file.write(password_info)
    file.close()

    email_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(screen1, text="Registration Sucess", fg="green", font=("calibri", 11), command=success()).pack()
    


def verify_user():
    email1 = email_verify.get()
    password1 = password_verify.get()
    #fp=open("my_2.txt","r")
    #lines1=fp.readlines()
    #__HOST = lines1[0].rstrip()
    #__USERNAME = lines1[1].rstrip()
    #__PASSWORD = lines1[2].rstrip()
    #__DATABASE = lines1[3].rstrip()
    #print(__HOST,__USERNAME,__PASSWORD,__DATABASE)
    #connection = connections(__HOST,__USERNAME,__PASSWORD,__DATABASE)
    connection=connections()
    #print("hello")
    ans=connection.my_verify_user(email1,password1)
    print(ans)   

    if ans is True:
        login_sucess()
    else:
        user_not_found()
        

def login_verify():
    email1 = email_verify.get()
    password1 = password_verify.get()
    email_entry1.delete(0, END)
    password_entry1.delete(0, END)

    f = open("Details.txt", "r")
    verify = (f.readlines())
    if (verify != ""):
        if email1 and password1 in verify:
            login_sucess()
        else:
            password_not_recognised()

    else:
        user_not_found()


def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register Here")
    screen1.geometry("350x350")

    global email
    global password
    global email_entry
    global password_entry
    email = StringVar()
    password = StringVar()

    Label(screen1, text="Please enter details below").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Email or Username* ").pack()

    email_entry = Entry(screen1, textvariable=email)
    email_entry.pack()
    Label(screen1, text="Password * ").pack()
    password_entry = Entry(screen1, textvariable=password)
    password_entry.pack()
    Label(screen1, text="").pack()
    Button(screen1, text="Register", bg="lightgreen", height="2", width="20", command=register_user).pack()


def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("350x350")
    Label(screen2, text="Please enter below Details").pack()
    Label(screen2, text="").pack()

    global email_verify
    global password_verify

    email_verify = StringVar()
    password_verify = StringVar()

    global email_entry1
    global password_entry1

    Label(screen2, text=" Email or Username* ").pack()
    email_entry1 = Entry(screen2, textvariable=email_verify)
    email_entry1.pack()
    Label(screen2, text="").pack()
    Label(screen2, text="Password * ").pack()
    password_entry1 = Entry(screen2, textvariable=password_verify)
    password_entry1.pack()
    Label(screen2, text="").pack()
    Button(screen2, text="Login", bg="aqua", height="2", width="20", command=verify_user).pack()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("450x400")
    screen.title("Intruder Detection and Automatic Email Alerting System")
    Label(text="Welcome\nto\nIntruder detection system ", bg="skyblue", width="300", height="5", font=("TimesNewRoman", 20)).pack()
    Label(text="").pack()
    Button(text="Login", bg="skyblue", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", bg="skyblue", height="2", width="30", command=register).pack()

    screen.mainloop()


def system():
    paths = glob.glob('C:\my_storage_in_c\YASH_NOTES_2nd_year\EDAI_Group_Project\EDAI_project_code\Images_Data_understanding\*')
    names = []
    images = []
    image_encodings = []
    image_names = []
    count_img = 0
    for i in paths:
        images.append(face_recognition.load_image_file(i))
        image_encodings.append(face_recognition.face_encodings(images[count_img])[0])
        image_names.append(i.split('\\')[-1].split('.')[0])
        count_img+=1
        print(image_names)

    count = 0
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        gray = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(gray)
        face_encodings = face_recognition.face_encodings(gray, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(image_encodings, face_encoding)
            name = 'Unknown'
            face_distances = face_recognition.face_distance(image_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = image_names[best_match_index]
            if(name=='Unknown'):
                cv2.imwrite('C:\my_storage_in_c\YASH_NOTES_2nd_year\EDAI_Group_Project\Edai\Intruder\intru-{}.jpg'.format(count),frame)
                count+=1
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 3)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow("output",frame)
        if(cv2.waitKey(1)==ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()    
    myPath = glob.glob('C:\my_storage_in_c\YASH_NOTES_2nd_year\EDAI_Group_Project\Edai\Intruder\*')
    global countFolder
    count=0
    for i in myPath:
        img = cv2.imread(i)
        #print(blur)
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.Laplacian(gray_img, cv2.CV_64F).var()
        if(count % 1 == 0 and blur > 320):
            cv2.imwrite("C:\my_storage_in_c\YASH_NOTES_2nd_year\EDAI_Group_Project\Edai\Intruder\intru-{}.jpg".format(count), img)
            count += 1


    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    
    f=open("my_1.txt","r")
    lines=f.readlines()
    username=lines[0]
    passwd=lines[1]

    
    #connection.__init__(__HOST,__USERNAME,__PASSWORD,__DATABASE)
    

    server.login(username,passwd)
 

    msg= MIMEMultipart()
    msg['from'] = username
    msg['to'] = ""
    msg['subject'] = "Images"
    text = "Check these sample unknown person images, if some thing *fishy!!* check intruder folder immediately"
    msg.attach(MIMEText(text))
    F = glob.glob("C:\my_storage_in_c\YASH_NOTES_2nd_year\EDAI_Group_Project\Edai\Intruder\*")
    for i in F:
        with open(i,'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('content-Disposition','attachment',filename='{}.jpg'.format(count+1))
                msg.attach(part)
    server.sendmail(username,lines[0],msg.as_string())

    f.close()


main_screen()
