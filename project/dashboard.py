from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.messagebox
import tkinter as tk
import mysql.connector
from room.room_install import room_installed_window
from room.room_available import room_available_window
from room.room_booked import room_occupied_window
import time, calendar, datetime

import cv2

DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "localhost"
DB_port = "3306"



class MainFrame:
    def __init__(self, dash):
        super().__init__()
        self.dash = dash
        dash.title("Iot-based Realtime Classroom Vacancy Monitoring & Reserve System")
        dash.geometry("1000x600")
        dash.resizable(False, False)
        global menu_bar    

        self.opened_windows = []
        
        def open_room_available_window():
            if self.opened_windows:
                self.opened_windows[-1].destroy()
            # Open the room installed window
            room_available_window1 = Toplevel(dash)
            room_available_window(room_available_window1)

        def open_room_installed_window():
            if self.opened_windows:
                self.opened_windows[-1].destroy()
            # Open the room installed window
            room_installed_window1 = Toplevel(dash)
            room_installed_window(room_installed_window1)

        def open_room_occupied_window():
            if self.opened_windows:
                self.opened_windows[-1].destroy()
            # Open the room installed window
            room_occupied_window1 = Toplevel(dash)
            room_occupied_window(room_occupied_window1)
        
        def default():
            global room_back, dashboard_icon, classroom_icon, account_icon

            img = Image.open('image/room.png')
            dashboard = Image.open('image/dashboard-icon.png')
            classroom = Image.open('image/classroom-icon.png')
            account = Image.open('image/account-icon.png')

            f2=Frame(dash, width=1000, height=600)
            f2.place(x=0, y=40)
            l2=Label(dash, text='Welcome to the System', fg='#2B3467', font=('Inter', 24, 'bold'))
            l2.place(x=300, y=50)

            room_back = ImageTk.PhotoImage(img.resize(size=(450, 330)))
            background = Label(f2, image=room_back)
            background.place(x=270, y=70)

            dashboard_icon = ImageTk.PhotoImage(dashboard.resize(size=(200, 80)))
            dashboard_icon_bg = Button(f2, image=dashboard_icon, border=0)
            dashboard_icon_bg.place(x=100, y=440)

            classroom_icon = ImageTk.PhotoImage(classroom.resize(size=(200, 80)))
            classroom_icon_bg = Button(f2, image=classroom_icon, border=0)
            classroom_icon_bg.place(x=400, y=440)

            account_icon = ImageTk.PhotoImage(account.resize(size=(200, 80)))
            account_icon_bg = Button(f2, image=account_icon, border=0)
            account_icon_bg.place(x=700, y=440)

        def multiple_window():
            global logo

            f1=Frame(dash, width=300, height=600, bg='#748299')

            button_pressed = False
            def on_enter(e):
                if not button_pressed:
                    e.widget.config(bg='#2B3467')

            def on_leave(e):
                if not button_pressed:
                    e.widget.config(bg='#748299')

            def dashboard_page():
                global user, reservation, today_reservation
                f1.destroy()

                def update_calendar():
                    year = time.localtime().tm_year
                    month = time.localtime().tm_mon
                    cal = calendar.monthcalendar(year, month)
                    # Update the label and text widget with the new calendar
                    calendar_label.config(text=calendar.month_name[month] + " " + str(year))
                    calendar_text.delete("1.0", tk.END)
                    for week in cal:
                        for day in week:
                            if day == 0:
                                calendar_text.insert(tk.END, "   ")
                            else:
                                calendar_text.insert(tk.END, str(day) + " ")
                            calendar_text.insert(tk.END, "\n")
    
                    # Schedule the function to run again at midnight
                    root.after(86400000, update_calendar)

            
                #icons
                user = ImageTk.PhotoImage(Image.open('image/user-pen.png').resize(size=(40, 40)))
                reservation = ImageTk.PhotoImage(Image.open('image/school1.png').resize(size=(40, 40)))
                today_reservation = ImageTk.PhotoImage(Image.open('image/presentation.png').resize(size=(40, 40)))

                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)
                l2=Label(dash, text='Dashboard', fg='#2B3467', font=('Inter', 24, 'bold'), bg='#d8dee8')
                l2.place(x=40, y=60)
                l2=Label(dash, text='Hello!, ', fg='#2B3467', font=('Inter', 16, 'bold'), bg='#d8dee8')
                l2.place(x=40, y=120)

                box1 = Frame(dash, width=200, height=150, bg='#2B3467')
                box1.place(x=40, y=170)
                user_image = Label(box1, image=user, bg='#2B3467').place(x=10, y=10)
                Label(box1, text='Total User: ', fg='#d8dee8', font=('Inter', 12, 'bold'), bg='#2B3467').place(x=10, y=55)

                box2 = Frame(dash, width=200, height=150, bg='#2B3467')
                box2.place(x=250, y=170)
                reservation_image = Label(box2, image=reservation, bg='#2B3467').place(x=10, y=10)
                Label(box2, text='Total Reservation: ', fg='#d8dee8', font=('Inter', 12, 'bold'), bg='#2B3467').place(x=10, y=55)

                box3 = Frame(dash, width=200, height=150, bg='#2B3467')
                box3.place(x=460, y=170)
                today_reservation_image = Label(box3, image=today_reservation, bg='#2B3467').place(x=10, y=10)
                Label(box3, text='Today Reservation: ', fg='#d8dee8', font=('Inter', 12, 'bold'), bg='#2B3467').place(x=10, y=55)

                #calendar display
                calendar_label = Label(f2, text='CALENDAR', fg='#2B3467', font=('Inter', 16, 'bold'), bg='#d8dee8')
                calendar_label.place(x=700, y=20)
                calendar_text = Text(f2, fg='#2B3467', font=('Inter', 12, 'bold'), bg='#d8dee8')
                calendar_text.place(x=700, y=30)
                #calendar frame
                #calendar_frame = Frame(f2, height=300, width=300, bg='#d8dee8')
                #calendar_frame.place(x=700, y=50)

                update_calendar()
                
            def classroom_page():
                global img1, img2, img3, dot

                f1.destroy()

                def number_rooms():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM room")
                    result = cursor.fetchone()
                    count = result[0]
                    return count
                
                def number_rooms_available():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM room WHERE status='available'")
                    result = cursor.fetchone()
                    count = result[0]
                    return count
                
                def number_rooms_occupied():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM room WHERE status='occupied'")
                    result = cursor.fetchone()
                    count = result[0]
                    return count
                
                def show_reservation():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    mycursor = conn.cursor()
                    mycursor.execute("SELECT id, name, account_type, event, time_start, time_end FROM reservation")
                    record = mycursor.fetchall()
                    conn.close()  
                    for i, (id, name, account_type, event, time_start, time_end) in enumerate(record, start=1):
                            listview.insert("", "end", values=(id, name, account_type, event, time_start, time_end))

                def populate_listview():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    mycursor = conn.cursor()

                    now = datetime.datetime.now()
                    current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

                    mycursor.execute("SELECT id, name, account_type, event, time_start, time_end FROM reservation")
                    records = mycursor.fetchall()

                    self.listview.delete(*self.listview.get_children())

                    for row in records:
                        time_end = row[5]
                        time_end_datetime = datetime.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
                        if time_end_datetime >= now:
                            self.listview.insert("", "end", values=row)
                    conn.close()

                
                dot = ImageTk.PhotoImage(Image.open('image/apps-add.png').resize(size=(20, 20)))

                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)
                l2=Label(dash, text='CLASSROOM', font=('Inter', 24, 'bold'), fg='#2B3467', bg='#d8dee8')
                l2.place(x= 395, y=60)

                #Time & Date Realtime
                label_date_now = Label(f2, text='', font=('Helvetica', 12, 'bold'), fg='#2B3467', bg='#d8dee8')
                label_date_now.place(x=50, y=20)
                label_time_now = Label(f2, text='', font=("Helvetica", 18, 'bold'), fg='#2B3467', bg='#d8dee8')
                label_time_now.place(x=50, y=40)

                #Classroom installed frame
                b1=Frame(f2, width=250, height=100, bg='#2B3467')
                b1.place(x=50, y=100)
                img1 = ImageTk.PhotoImage(Image.open('image/school.png').resize(size=(50, 50)))
                classroom_img=Label(b1, image=img1, bg='#2B3467', )
                classroom_img.place(x=10, y=20)
                class_installed = Label(b1, text='Room Installed', font=('Inter', 12, 'bold'), bg='#2B3467', fg='white')
                class_installed.place(x=75, y=10)
                menu=Button(b1, image=dot, text='Open', border=0, bg='#2B3467', activebackground='#2B3467', command=open_room_installed_window)
                menu.place(x=210, y=10)
                # Display the number of rooms installed
                num_rooms_installed = number_rooms()
                Label(b1, text=f": {num_rooms_installed}", font=('Inter', 24, 'bold'), bg='#2B3467', fg='white').place(x=80, y=30)


                #Classroom available frame
                b12=Frame(f2, width=250, height=100, bg='#2B3467')
                b12.place(x=375, y=100)
                img2 = ImageTk.PhotoImage(Image.open('image/comment-user.png').resize(size=(50, 50)))
                classroom_img1=Label(b12, image=img2, bg='#2B3467')
                classroom_img1.place(x=10, y=20)
                class_available = Label(b12, text='Room Available', font=('Inter', 12, 'bold'), bg='#2B3467', fg='white')
                class_available.place(x=75, y=10)
                menu=Button(b12, image=dot, text='Open', border=0, bg='#2B3467', activebackground='#2B3467', command=open_room_available_window)
                menu.place(x=210, y=10)
                # Display the number of rooms installed
                num_rooms_available = number_rooms_available()
                Label(b12, text=f": {num_rooms_available}", font=('Inter', 24, 'bold'), bg='#2B3467', fg='white').place(x=80, y=30)


                #classroom booked frame
                b13=Frame(f2, width=250, height=100, bg='#2B3467')
                b13.place(x=700, y=100)
                img3 = ImageTk.PhotoImage(Image.open('image/user-time.png').resize(size=(50, 50)))
                classroom_img2=Label(b13, image=img3, bg='#2B3467')
                classroom_img2.place(x=10, y=20)
                class_book = Label(b13, text='Room Booked', font=('Inter', 12, 'bold'), bg='#2B3467', fg='white')
                class_book.place(x=75, y=10)
                menu=Button(b13, image=dot, text='Open', border=0, bg='#2B3467', activebackground='#2B3467', command=open_room_occupied_window)
                menu.place(x=205, y=10)
                num_rooms_occupied = number_rooms_occupied()
                Label(b13, text=f": {num_rooms_occupied}", font=('Inter', 24, 'bold'), bg='#2B3467', fg='white').place(x=80, y=30)


                #List of booked room
                list_room_reservation = Frame(dash, width=900, height=280, bg='white')
                list_room_reservation.place(x=50, y=280)
                cols = ('id', 'Name', 'Account Type', 'Room #','Event','Subject Code', 'No. of Hour' ,'Time Start' ,'Time end')
                listview = ttk.Treeview(list_room_reservation, columns=cols, show='headings', height=13)
                listview.pack(expand=False)
                listview_style = ttk.Style(list_room_reservation)
                listview_style.theme_use('default')
                listview_style.configure('.', font=('Helvetica', 10))
                listview_style.configure('Treeview.Heading', foreground='#2B3467', font=('Helvetica', 10,'bold'))

                for col in cols:
                    listview.heading(col, text=col)
                    if col =='id':
                        listview.column(col, width=10)
                    elif col == 'Name':
                        listview.column(col, width=150)  # adjust the width of 'id' column
                    elif col == 'Account Type':
                        listview.column(col, width=150)
                    elif col == 'Room Number':
                        listview.column(col, width=20)
                    elif col == 'No. of Hour':
                        listview.column(col, width=100)
                    elif col == 'Event':
                        listview.column(col, width=100)
                    elif col == 'Subject Code':
                        listview.column(col, width=100)
                    elif col == 'Time Start':
                        listview.column(col, width=100)
                    elif col == 'Time End':
                        listview.column(col, width=100)
                    else:
                        listview.column(col, width=94) 
                    listview.grid(row=1, column=7, columnspan=1)
                    listview.place(x=0, y=0)   

                def update_clock():
                    hour = time.strftime("%I")
                    minute = time.strftime("%M")  
                    second = time.strftime("%S")
                    am_pm = time.strftime("%p")
                    day = time.strftime("%A")

                    label_time_now.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
                    label_time_now.after(1000, update_clock)
                    label_date_now.config(text=day)

                def update():
                    label_date_now.config(text="")
                    label_time_now.config(text="")
                update_clock()
                show_reservation()
                populate_listview()

            #Account page where you can add user for mobile application
            def account_page():
                global a
                global a1
                global a2
                global a3
                global a4
                global listclass

                f1.destroy()
                def GetValue(event):
                    row_id = listview.selection()[0]
                    select = listview.set(row_id)
                    a1.delete(0, END)
                    a2.delete(0, END)
                    a3.delete(0, END)
                    a4.delete(0, END)
                    a1.insert(0, select['Surname'])
                    a2.insert(0, select['Firstname'])
                    a3.insert(0, select['Email'])
                    a4.insert(0, select['Password'])
                    listclass.set(select['Account_type'])
                        
                #Add account and stored to the database
                def add():
                    surname = a1.get()
                    firstname = a2.get()
                    email = a3.get()
                    password = a4.get()
                    account_type = listclass.get()

                    if surname == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Surname')
                    if firstname == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Firstname')
                    if email == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Email')
                    if password == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Password')
                    if surname != '' and firstname != '' and email !='' and password !='':
                        conn = mysql.connector.connect(
                            host = DB_hostname,
                            user = DB_username,
                            password = DB_password,
                            database = DB_database,
                            port = DB_port
                            )
                        mycursor=conn.cursor()

                        try:
                            mycursor.execute("INSERT INTO mobile_user (surname, firstname, email, password, account_type) VALUES (%s, %s, %s, %s, %s) ",
                                (surname, firstname, email, password, account_type))
                            conn.commit()
                            tkinter.messagebox.showinfo('', 'Adding account success')
                            a1.delete(0, END)
                            a2.delete(0, END)
                            a3.delete(0, END)
                            a4.delete(0, END)
                            a1.focus_set()
             
                            mycursor.execute("SELECT id, surname, firstname, email, password, account_type FROM mobile_user")
                            records = mycursor.fetchall()
                            print(f"adding records with surname {surname}")
                            print(records)
                            listview.delete(*listview.get_children())
                            for i, (id, surname, firstname, email, password, account_type) in enumerate(records, start=1):
                                listview.insert("", "end", values=(id, surname, firstname, email, password, account_type))
                        except Exception as error:
                            print(error)
                        conn.rollback()
                        conn.close()

                #Update function for mobile user
                def update():
                    id=a.get()
                    surname = a1.get()
                    firstname = a2.get()
                    email = a3.get()
                    password = a4.get()
                    account_type = listclass.get()
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    mycursor = conn.cursor()

                    try:
                        mycursor.execute("UPDATE mobile_user SET firstname = %s, email = %s, password = %s, account_type = %s WHERE surname = %s",
                            (firstname, email, password, account_type, surname))
                        conn.commit()
                        tkinter.messagebox.showinfo("information", "Record updated successfully...")
                        a1.delete(0, END)
                        a2.delete(0, END)
                        a3.delete(0, END)
                        a4.delete(0, END)
                        listview.delete(*listview.get_children())
                        a1.focus_set()

                        # Update the Treeview after the database update
                        mycursor.execute("SELECT id, surname, firstname, email, password, account_type FROM mobile_user")
                        records = mycursor.fetchall()
                        print(f"Updating records with surname {surname}")
                        print(records)
                        listview.delete(*listview.get_children())
                        for i, (id, surname, firstname, email, password, account_type) in enumerate(records, start=1):
                            listview.insert("", "end", values=(id, surname, firstname, email, password, account_type))
                    except Exception as e:
                        print(e)
                        conn.rollback()
                    finally:
                        conn.close()
                    
                #delete function for mobile_user
                def delete():
                    surname = a1.get()
                    if not surname:
                        tkinter.messagebox.showerror("Error", "No surname entered. Please enter a surname to delete.")
                        return
                    else:
                        conn = mysql.connector.connect(
                            host = DB_hostname,
                            user = DB_username,
                            password = DB_password,
                            database = DB_database,
                            port = DB_port
                            )
                        mycursor=conn.cursor()
 
                        try:
                            mycursor.execute("DELETE FROM mobile_user WHERE surname = %s", (surname, ))
                            conn.commit()
                            tkinter.messagebox.showinfo("information", "Record deleted successfully...")
                            a.delete(0, END)
                            a1.delete(0, END)
                            a2.delete(0, END)
                            a3.delete(0, END)
                            a4.delete(0, END)
                            a1.focus_set()

                            mycursor.execute("SELECT id, surname, firstname, email, password, account_type FROM mobile_user")
                            records = mycursor.fetchall()
                            print(f"Deleting records with surname {surname}")
                            print(records)
                            listview.delete(*listview.get_children())
                            for i, (id, surname, firstname, email, password, account_type) in enumerate(records, start=1):
                                listview.insert("", "end", values=(id, surname, firstname, email, password, account_type))
 
                        except Exception as e:
                            print(e)
                            conn.rollback()
                        finally:
                            conn.close()

                #display the mobile user from database
                def show():
                    conn = mysql.connector.connect(
                        host=DB_hostname,
                        user=DB_username,
                        password=DB_password,
                        database=DB_database,
                        port=DB_port
                    )
                    mycursor = conn.cursor()
                    mycursor.execute("SELECT id, surname, firstname, email, password, account_type FROM mobile_user")
                    record = mycursor.fetchall()
                    conn.close()  
                    for i, (id, surname, firstname, email, password, account_type) in enumerate(record, start=1):
                            listview.insert("", "end", values=(id, surname, firstname, email, password, account_type))  

                #def search():
                    #selected = search_drop.get()
                    #if selected == "Search by...":
                    #if selected == "Lastname":
                    #if selected == "Firstname":


                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)

                Label(f2, text='Accounts', font=('Inter', 24, 'bold'), bg='#d8dee8', fg='#2B3467').place(x=35, y=5)


                bg = Frame(f2, width=335, height=480, bg='#1151b8', padx=20)
                bg.place(x=35, y=50)

                Add = tk.Label(bg, text='Add user', font=('Inter', 16, 'bold'), fg='#262626', bg='#d8dee8')
                Add.place(x=100, y=10)

                a=tk.Label(bg, text='Id', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
                a.place(x=5, y=50)
                a=Entry(bg, font=('Inter', 14), width=25)
                a.place(x=5, y=80)

                a1=tk.Label(bg, text='Surname', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
                a1.place(x=5, y=50)
                a1=Entry(bg, font=('Inter', 14), width=25)
                a1.place(x=5, y=80)

                a2=tk.Label(bg, text='Firstname', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
                a2.place(x=5, y=110)
                a2=Entry(bg, font=('Inter', 14), width=25)
                a2.place(x=5, y=140)

                a3=tk.Label(bg, text='Email', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
                a3.place(x=5, y=170)
                a3=Entry(bg, font=('Inter', 14), width=25)
                a3.place(x=5, y=200)

                a4=tk.Label(bg, text='Password', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
                a4.place(x=5, y=230)
                a4=Entry(bg, font=('Inter', 14), width=25, show='*')
                a4.place(x=5, y=260)

                lists = ['Instructor', 'Classroom Officer']
                listclass = StringVar(bg)
                listclass.set("You are a: ")
                a5 = OptionMenu(bg, listclass, *lists)
                a5.place(x=5, y=310, width=190)

                f3 = Frame(dash, width=600, height=480, border=1)
                f3.place(x=380, y=90)

                submit = Button(bg, text='Add', fg='white', border=0, bg='#2B3467', width=10, font=('Inter', 16, 'bold'),command=add)
                submit.place(x=50, y=380)

                Update = Button(f3, text='Update', fg='white', border=0, bg='#2B3467', width=10, font=('Inter', 16, 'bold'),command=update)
                Update.place(x=30, y=380)

                Delete = Button(f3, text='Delete', fg='white', border=0, bg='#2B3467', width=10, font=('Inter', 16, 'bold'),command=delete)
                Delete.place(x=300, y=380)

                cols = ('id','Surname', 'Firstname', 'Email', 'Password', 'Account_type')
                listview = ttk.Treeview(f3, columns=cols, show='headings')
                listview.bind('<Double-Button-1>', GetValue)
                listview_style = ttk.Style(f3)
                listview_style.theme_use('default')
                listview_style.configure('.', font=('Helvetica', 10))
                listview_style.configure('Treeview.Heading', foreground='#2B3467', font=('Helvetica', 10,'bold'))

                for col in cols:
                    listview.heading(col, text=col)
                    if col == 'id':
                        listview.column(col, width=15)
                    elif col == 'Surname':
                        listview.column(col, width=70)
                    elif col == 'Firstname':
                        listview.column(col, width=70)
                    elif col == 'Email':
                        listview.column(col, width=160)
                    elif col == 'Password':
                        listview.column(col, width=100)
                    else:
                        listview.column(col, width=180)
                    listview.grid(row=1, column=6, columnspan=1)
                    listview.place(x=0, y=0)
                show()

            def faq_page():
                f1.destroy()
                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)
                l2=Label(dash, text='Welcome to the System', fg='#232323', font=('Inter', 18, 'bold'), bg='#d8dee8')
                l2.place(x=150, y=60)

            def hide_indicator():
                home_indicator.config(bg='#748299')
                classroom_indicator.config(bg='#748299')
                account_indicator.config(bg='#748299')
                faq_indicator.config(bg='#748299')

            def indicator(lb, page):
                hide_indicator()
                lb.configure(bg="red")
                page()

            def logout():
                # ask user for confirmation
                confirm = tkinter.messagebox.askyesno("Log out", "Are you sure you want to log out?")
                if confirm:
                    root.destroy()
           
            def dele():
                 f1.destroy()
            global cross

            logo = ImageTk.PhotoImage(Image.open('image/bisu-logo.png').resize(size=(80,80)))
            room = Label(f1, image=logo, bg='#748299')
            room.place(x=105, y=10)

            home = tk.Button(f1, text='Dashboard',border=0, fg='white', bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=lambda: indicator(home_indicator, dashboard_page))
            home.place(x=15, y=100)
            home_indicator = tk.Label(f1, text='', bg='#748299')
            home_indicator.place(x=15, y=100, width=5, height=38)
            home.bind('<Enter>', on_enter)
            home.bind('<Leave>', on_leave)
           
            classroom = tk.Button(f1, text='Classrooms',border=0,fg='white' ,bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=lambda: indicator(classroom_indicator, classroom_page))
            classroom.place(x=15, y=150)
            classroom_indicator = tk.Label(f1, text='', bg='#748299')
            classroom_indicator.place(x=15, y=150, width=5, height=38)
            classroom.bind('<Enter>', on_enter)
            classroom.bind('<Leave>', on_leave)

            account = tk.Button(f1, text='Accounts',border=0,fg='white' ,bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=lambda: indicator(account_indicator, account_page))
            account.place(x=15, y=200)
            account_indicator = tk.Label(f1, text='', bg='#748299')
            account_indicator.place(x=15, y=200, width=5, height=38)
            account.bind('<Enter>', on_enter)
            account.bind('<Leave>', on_leave)

            faq = tk.Button(f1, text='Faq',border=0, bg='#748299',fg='white' , width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=lambda: indicator(faq_indicator, faq_page))
            faq.place(x=15, y=250)
            faq_indicator = tk.Label(f1, text='', bg='#748299')
            faq_indicator.place(x=15, y=250, width=5, height=38)
            faq.bind('<Enter>', on_enter)
            faq.bind('<Leave>', on_leave)

            quit1 = tk.Button(f1, text='Log out',fg='white',border=0,bg='#2B3467', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=logout)
            quit1.place(x=15, y=500)
            f1.place(x=0, y=0)

            cross = ImageTk.PhotoImage(Image.open('image/cross.png'))
            cross_Button = Button(f1, image=cross, command=dele, border=1, activebackground='#748299')
            cross_Button.place(x=10, y=10)
            cross_Button.bind('<Enter>', on_enter)
            cross_Button.bind('<Leave>', on_leave)
            
        
        menu_bar = ImageTk.PhotoImage(Image.open('image/menu-burger.png'))
        Button(dash, image=menu_bar, command=multiple_window, text='Open', border=0, activebackground='#748299').place(x=10, y=10)

        default()

root = Tk()
mainframe = MainFrame(root)
root.mainloop()
