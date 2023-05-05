from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

if not firebase_admin._apps:
    # Initialize the app with a service account
    cred = credentials.Certificate('D:/DOWNLOADS/thesismobileapp-304b0-firebase-adminsdk-2eufd-4703063921.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://thesismobileapp-304b0-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
    
class LoginPage:
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("Iot-based Realtime Classroom Vacancy Monitoring & Reserve System")
        master.geometry("800x460")
        master.resizable(False, False)
        
        global banner

        window_icon = ImageTk.PhotoImage(Image.open('image/bisu-logo.png'))
        master.iconphoto(False, window_icon)
        def sign_in():
            # Get a reference to your database
            ref = db.reference('/admin')

            username=user.get()
            password=code.get()

            # Get the user from the database
            result = ref.order_by_child('username').equal_to(username).get()

            if result:
                for key, value in result.items():
                    # Check the password
                    if value['password'] == password:
                        tkinter.messagebox.showinfo('', 'Log in Success')
                        root.destroy()
                        import dashboard
                    else:
                        tkinter.messagebox.showinfo('', 'Incorrect password')
            else:
                tkinter.messagebox.showinfo('', 'Incorrect username')
        
        
        frame1=Frame(root, width=450, height=350)
        frame1.place(x=10, y=10)
        
        banner = ImageTk.PhotoImage(Image.open('image/bisu-banner.png'))
        room = Label(frame1, image=banner)
        room.place(x=20, y=65)

        title=Label(frame1, text="Classroom Vacancy", fg="#2B3467", font=('Inter', 24, 'bold'))
        title.place(x=20, y=190)
        title1=Label(frame1, text="Monitoring & Reserve", fg="#2B3467", font=('Inter', 24, 'bold'))
        title1.place(x=20, y=230)
        title2=Label(frame1, text="System", fg="#2B3467", font=('Inter', 24, 'bold'))
        title2.place(x=20, y=270)


        frame=Frame(root, width=300, height=350, bg='#748299')
        frame.place(x=450, y=65)

        #header
        heading=Label(frame, text='Sign in', fg='white', font=('Inter', 23, 'bold'), bg='#748299')
        heading.place(x=100, y=5)

        #Form Email
        def on_enter(e):
            user.delete(0, 'end')

        def on_leave(e):
            name=user.get()
            if name=='':
                user.insert(0, 'Enter email')

        user=tk.Label(frame, text='Email', fg='white', font=('Inter', 14, 'bold'), bg='#748299' ).place(x=20, y=58)
        user = Entry(frame, width=25, fg='white', border=0, font=('Inter', 14), bg='#748299')
        user.place(x=25, y=85,)
        user.insert(0, 'enter email')
        user.bind('<FocusIn>', on_enter)
        user.bind('<FocusOut>', on_leave)
        Frame(frame, width=255, height=1, bg='black').place(x=25, y=107)

        #Form Password
        def on_enter(e):
            code.delete(0, 'end')

        def on_leave(e):
            name=code.get()
            if name=='':
                code.insert(0, 'enter password')
        code = Label(frame, text='Password', fg='white', font=('Inter', 14, 'bold'), bg='#748299').place(x=20, y=123)
        code = Entry(frame, width=25, fg='white', border=0, font=('Inter', 14), show='*', bg='#748299')
        code.place(x=25, y=155,)
        code.insert(0, 'Enter password')
        code.bind('<FocusIn>', on_enter)
        code.bind('<FocusOut>', on_leave)
        Frame(frame, width=255, height=1, bg='black').place(x=25, y=177)
        
        def on_enter(e):
            e.widget.config(bg='#d8dee8', fg='#2B3467')

        def on_leave(e):
            e.widget.config(bg='#2B3467', fg='white')

        #button log in
        signin_button = Button(frame, width=19, cursor='hand2', background='#2B3467', border=0, text="Sign in", fg="white", font=('Inter', 16, 'bold'), command=sign_in, )
        signin_button.place(x=25, y=204)
        signin_button.bind('<Enter>', on_enter)
        signin_button.bind('<Leave>', on_leave)
        Button(frame, text='Forgot password?', bg='#748299', font=('Inter', 12), border=0, fg='white', cursor="hand2").place(x=90, y= 260)

if __name__ == '__main__':
    root = Tk()
    login_page = LoginPage(root)
    root.mainloop()