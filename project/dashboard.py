from tkinter import *
from tkinter import ttk, END
from PIL import ImageTk, Image
import tkinter.messagebox
import tkinter as tk
from room.room_install import room_installed_window
from room.room_available import room_available_window
from room.room_booked import room_occupied_window
import time, calendar, datetime
from datetime import datetime
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
            room_available_window1.protocol("WM_DELETE_WINDOW", lambda: (tkinter.messagebox.showinfo("Message", "Room Available window is closed."), room_available_window1.destroy()))

        def open_room_installed_window():
            if self.opened_windows:
                self.opened_windows[-1].destroy()
            # Open the room installed window
            room_installed_window1 = Toplevel(dash)
            room_installed_window(room_installed_window1)
            room_installed_window1.protocol("WM_DELETE_WINDOW", lambda: (tkinter.messagebox.showinfo("Message", "Room Installed window is closed."), room_installed_window1.destroy()))

        def open_room_occupied_window():
            if self.opened_windows:
                self.opened_windows[-1].destroy()
            # Open the room installed window
            room_occupied_window1 = Toplevel(dash)
            room_occupied_window(room_occupied_window1)
            room_occupied_window1.protocol("WM_DELETE_WINDOW", lambda: (tkinter.messagebox.showinfo("Message", "Room Occupied window is closed."), room_occupied_window1.destroy()))
        
        def default():
            global room_back, dashboard_icon, classroom_icon, account_icon, about_icon

            img = Image.open('image/room.png')
            dashboard = Image.open('image/dashboard-icon.png')
            classroom = Image.open('image/classroom-icon.png')
            account = Image.open('image/account-icon.png')
            about = Image.open('image/about-icon.png')

            f2=Frame(dash, width=1000, height=600)
            f2.place(x=0, y=40)
            l2=Label(dash, text='Welcome to the System', fg='#2B3467', font=('Inter', 24, 'bold'))
            l2.place(x=300, y=50)

            room_back = ImageTk.PhotoImage(img.resize(size=(450, 330)))
            background = Label(f2, image=room_back)
            background.place(x=270, y=70)

            dashboard_icon = ImageTk.PhotoImage(dashboard.resize(size=(200, 80)))
            dashboard_icon_bg = Button(f2, image=dashboard_icon, border=0)
            dashboard_icon_bg.place(x=70, y=440)

            classroom_icon = ImageTk.PhotoImage(classroom.resize(size=(200, 80)))
            classroom_icon_bg = Button(f2, image=classroom_icon, border=0)
            classroom_icon_bg.place(x=285, y=440)

            account_icon = ImageTk.PhotoImage(account.resize(size=(200, 80)))
            account_icon_bg = Button(f2, image=account_icon, border=0)
            account_icon_bg.place(x=500, y=440)

            about_icon = ImageTk.PhotoImage(about.resize(size=(200, 80)))
            about_icon_bg = Button(f2, image=about_icon, border=0)
            about_icon_bg.place(x=715, y=440)


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
                f1.destroy()

                global room_back, dashboard_icon, classroom_icon, account_icon, about_icon

                img = Image.open('image/room.png')
                dashboard = Image.open('image/dashboard-icon.png')
                classroom = Image.open('image/classroom-icon.png')
                account = Image.open('image/account-icon.png')
                about = Image.open('image/about-icon.png')

                f2=Frame(dash, width=1000, height=600)
                f2.place(x=0, y=40)
                l2=Label(dash, text='Welcome to the System', fg='#2B3467', font=('Inter', 24, 'bold'))
                l2.place(x=300, y=50)

                room_back = ImageTk.PhotoImage(img.resize(size=(450, 330)))
                background = Label(f2, image=room_back)
                background.place(x=270, y=70)

                dashboard_icon = ImageTk.PhotoImage(dashboard.resize(size=(200, 80)))
                dashboard_icon_bg = Button(f2, image=dashboard_icon, border=0, command=dashboard_page)
                dashboard_icon_bg.place(x=70, y=440)

                classroom_icon = ImageTk.PhotoImage(classroom.resize(size=(200, 80)))
                classroom_icon_bg = Button(f2, image=classroom_icon, border=0, command=classroom_page)
                classroom_icon_bg.place(x=285, y=440)

                account_icon = ImageTk.PhotoImage(account.resize(size=(200, 80)))
                account_icon_bg = Button(f2, image=account_icon, border=0, command= account_page)
                account_icon_bg.place(x=500, y=440)

                about_icon = ImageTk.PhotoImage(about.resize(size=(200, 80)))
                about_icon_bg = Button(f2, image=about_icon, border=0, command= about_page)
                about_icon_bg.place(x=715, y=440)
                
            def classroom_page():
                global img1, img2, img3, dot

                f1.destroy()
                
                def number_rooms():
                    ref = db.reference('Room')
                    data = ref.get()
                    if data is None:
                        return 0
                    count = len(data)
                    return count
                
                def number_rooms_available():
                    ref = db.reference('Room')
                    data = ref.get()
                    if isinstance(data, str):
                        data = json.loads(data)
                    count = sum(1 for room in data.values() if room.get('Availability') == True)
                    return count

            
                def number_rooms_occupied():
                    ref = db.reference('Room')
                    data = ref.get()
                    if isinstance(data, str):
                        data = json.loads(data)
                    count = sum(1 for room in data.values() if room.get('Availability') == False)
                    return count
                
                def show_reservation():
                    ref = db.reference('Room')
                    rooms_snapshot = ref.get()

                    if not rooms_snapshot:
                        print("Error: Unable to retrieve rooms data from the database")
                        return

                    if not isinstance(rooms_snapshot, dict):
                        print("Error: Rooms data is not in the expected format")
                        return

                    for room_id, room_data in rooms_snapshot.items():
                        if "Room Number" in room_data:
                            room_number = room_data["Room Number"]
                        else:
                            print(f"Error: Room number not found for room {room_id}")
                            continue

                        if "Reserve" in room_data:
                            reserve_data = room_data["Reserve"]

                            name = reserve_data.get("FullName")
                            date = reserve_data.get("Date")
                            event = reserve_data.get("Event")
                            subject_code = reserve_data.get("SubjectCode")
                            time_start = reserve_data.get("TimeStart")
                            time_end = reserve_data.get("TimeEnd")

                            if subject_code is None:
                                print(f"Error: Subject code not found for room {room_number}")
                                continue
                            
                            current_time = datetime.now().strftime('%H:%M')
                            
                            # Check if reservation time has not started yet
                            if current_time < time_start:
                                # Insert the reservation data to the listview
                                self.listview.insert("", "end", values=(name, date, room_number, event, subject_code, time_start, time_end))
                            else:
                                # Reservation time has already started, remove it from the listview
                                for item in self.listview.get_children():
                                    if self.listview.item(item)['values'][0] == name and self.listview.item(item)['values'][2] == room_number:
                                        self.listview.delete(item)
                                        break

                   
                def show_reservation1():
                    ref = db.reference('Room')
                    rooms_snapshot = ref.get()

                    if not rooms_snapshot:
                        print("Error: Unable to retrieve rooms data from the database")
                        return

                    if not isinstance(rooms_snapshot, dict):
                        print("Error: Rooms data is not in the expected format")
                        return

                    for room_id, room_data in rooms_snapshot.items():
                        if "Room Number" in room_data:
                            room_number = room_data["Room Number"]
                        else:
                            print(f"Error: Room number not found for room {room_id}")
                            continue

                        if "Reserve" in room_data:
                            reserve_data = room_data["Reserve"]

                            name = reserve_data.get("FullName")
                            date = reserve_data.get("Date")
                            event = reserve_data.get("Event")
                            subject_code = reserve_data.get("SubjectCode")
                            time_start = reserve_data.get("TimeStart")
                            time_end = reserve_data.get("TimeEnd")

                            if subject_code is None:
                                print(f"Error: Subject code not found for room {room_number}")
                                continue

                            current_time = datetime.now().strftime('%H:%M')

                            # Check if the reservation has already ended
                            if time_end is not None and current_time >= time_end:
                                # Remove the reservation from the database
                                room_ref = db.reference(f"Room/{room_id}")
                                room_ref.child("Reserve").delete()
                                continue

                            # Check if the current time is within the reserved time range
                            if current_time >= time_start:
                                # Insert the reservation data to the listview
                                self.listview.insert("", "end", values=(name, date, room_number, event, subject_code, time_start, time_end))
         

                def GetValue(event):
                    # get the selected row from the listview
                    row_id = listview.selection()[0]
                    select = listview.item(row_id, "values")
                    a1.delete(0, END)
                    a1.insert(0, select[0])


                def delete_selected_reservation():
                    fullname = a1.get() # get the full name entered by the user
                    if not fullname:
                        tkinter.messagebox.showwarning("No Item Selected", "Please enter a full name to delete.")
                        return
                    
                    # Connect to Firebase database
                    ref = db.reference('Room')
                    
                    try:
                        # Search for the record with the given full name in the Firebase database
                        records = ref.order_by_child('Reserve/FullName').equal_to(fullname).get()
                        if records:
                            # If a matching record is found, delete the 'Reserve' node only
                            record_key = list(records.keys())[0]
                            ref.child(record_key).child('Reserve').delete()
                            
                            # Show a success message and clear the entry box
                            tkinter.messagebox.showinfo("Reservation Deleted", f"The reservation for {fullname} has been deleted.")
                            a1.delete(0, END)
                            
                            # Update the listview to remove the deleted item
                            for item in self.listview.get_children():
                                item_data = self.listview.item(item, "values")
                                if item_data[0] == fullname:
                                    self.listview.delete(item)
                                    break
                        else:
                            # If no matching record is found, show a warning message
                            tkinter.messagebox.showwarning("Reservation Not Found", f"No reservation found for {fullname}.")
                    except Exception as e:
                        print(e)

                dot = ImageTk.PhotoImage(Image.open('image/apps-add.png').resize(size=(20, 20)))

                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)
                l2=Label(dash, text='CLASSROOMS', font=('Inter', 24, 'bold'), fg='#2B3467', bg='#d8dee8')
                l2.place(x= 385, y=40)

                #Time & Date Realtime
                label_date_now = Label(f2, text='', font=('Helvetica', 12, 'bold'), fg='#2B3467', bg='#d8dee8')
                label_date_now.place(x=50, y=0)
                label_time_now = Label(f2, text='', font=("Helvetica", 18, 'bold'), fg='#2B3467', bg='#d8dee8')
                label_time_now.place(x=50, y=20)

                #Classroom installed frame
                b1=Frame(f2, width=250, height=100, bg='#2B3467')
                b1.place(x=50, y=55)
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
                b12.place(x=375, y=55)
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
                b13.place(x=700, y=55)
                img3 = ImageTk.PhotoImage(Image.open('image/user-time.png').resize(size=(50, 50)))
                classroom_img2=Label(b13, image=img3, bg='#2B3467')
                classroom_img2.place(x=10, y=20)
                class_book = Label(b13, text='Room Booked', font=('Inter', 12, 'bold'), bg='#2B3467', fg='white')
                class_book.place(x=75, y=10)
                menu=Button(b13, image=dot, text='Open', border=0, bg='#2B3467', activebackground='#2B3467', command=open_room_occupied_window)
                menu.place(x=205, y=10)
                num_rooms_occupied = number_rooms_occupied()
                Label(b13, text=f": {num_rooms_occupied}", font=('Inter', 24, 'bold'), bg='#2B3467', fg='white').place(x=80, y=30)

                delete_button = tk.Button(dash, text="Delete", command=delete_selected_reservation, font=('Inter', 10))
                delete_button.place(x=900, y= 200)
                a1=Entry(dash ,font=('Inter', 14), width=15)
                a1.place(x=720, y=200)

                Label(f2, text='List of Upcoming Reservation', font=('Helvetica', 12, 'bold'), fg='#2B3467', bg='#d8dee8').place(x=50, y=165)

                list_room_reservation = Frame(dash, width=900, height=162, bg='white')
                list_room_reservation.place(x=50, y=230)
                cols = ('Name', 'Date', 'Room #','Event','Subject Code','Time Start' ,'Time end')
                listview = ttk.Treeview(list_room_reservation, columns=cols, show='headings', height=7)
                listview.pack(expand=False)
                listview_style = ttk.Style(list_room_reservation)
                listview_style.theme_use('default')
                listview_style.configure('.', font=('Helvetica', 10))
                listview_style.configure('Treeview.Heading', foreground='#2B3467', font=('Helvetica', 10,'bold'))

                for col in cols:
                    listview.heading(col, text=col, anchor='center')
                    if col == 'Name':
                        listview.column(col, width=150, anchor='center')  
                    elif col == 'Date':
                        listview.column(col, width=150, anchor='center')
                    elif col == 'Room Number':
                        listview.column(col, width=20, anchor='center')
                    elif col == 'Event':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Subject Code':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Time Start':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Time End':
                        listview.column(col, width=90, anchor='center')
                    else:
                        listview.column(col, width=149, anchor='center') 
                    listview.grid(row=1, column=7, columnspan=1)
                    listview.place(x=0, y=0)   
                
                self.listview = listview
                show_reservation()

                Label(f2, text='List of Current Reservation', font=('Helvetica', 12, 'bold'), fg='#2B3467', bg='#d8dee8').place(x=50, y=355)

                list_room_reservation = Frame(dash, width=900, height=162, bg='white')
                list_room_reservation.place(x=50, y=420)
                cols = ('Name', 'Date', 'Room #','Event','Subject Code','Time Start' ,'Time end')
                listview = ttk.Treeview(list_room_reservation, columns=cols, show='headings', height=7)
                listview.pack(expand=False)
                listview.bind('<Double-Button-1>', GetValue)
                listview_style = ttk.Style(list_room_reservation)
                listview_style.theme_use('default')
                listview_style.configure('.', font=('Helvetica', 10))
                listview_style.configure('Treeview.Heading', foreground='#2B3467', font=('Helvetica', 10,'bold'))

                for col in cols:
                    listview.heading(col, text=col, anchor='center')
                    if col == 'Name':
                        listview.column(col, width=150, anchor='center')  
                    elif col == 'Date':
                        listview.column(col, width=150, anchor='center')
                    elif col == 'Room Number':
                        listview.column(col, width=20, anchor='center')
                    elif col == 'Event':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Subject Code':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Time Start':
                        listview.column(col, width=100, anchor='center')
                    elif col == 'Time End':
                        listview.column(col, width=90, anchor='center')
                    else:
                        listview.column(col, width=149, anchor='center') 
                    listview.grid(row=1, column=7, columnspan=1)
                    listview.place(x=0, y=0)   
                
                self.listview = listview
                show_reservation1()
            
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
                    a3.insert(0, select['Username'])
                    a4.insert(0, select['Password'])
                    listclass.set(select['Account_type'])

                #Add account and stored to the database
                def add():
                    surname = a1.get()
                    firstname = a2.get()
                    username = a3.get()
                    password = a4.get()
                    account_type = listclass.get()

                    if surname == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Surname')
                    if firstname == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Firstname')
                    if username == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Username')
                    if password == '':
                        tkinter.messagebox.showinfo('Alert', 'Please Enter your Password')
                    if surname != '' and firstname != '' and username !='' and password !='':
                        db_ref = db.reference('mobile_user')
                        try:
                            # Create a new user object to add to the database
                            new_user = {
                                'surname': surname,
                                'firstname': firstname,
                                'username': username,
                                'password': password,
                                'account_type': account_type
                            }

                            # Push the new user object to the Firebase Realtime Database
                            db_ref.push(new_user)

                            tkinter.messagebox.showinfo('', 'Adding account success')
                            a1.delete(0, END)
                            a2.delete(0, END)
                            a3.delete(0, END)
                            a4.delete(0, END)
                            a1.focus_set()

                            # Get all the users from the Firebase Realtime Database
                            records = db_ref.get()
                            if records is None:
                                raise ValueError('No data retrieved from Firebase')
                            
                            print(f"adding records with surname {surname}")
                            print(records)

                            listview.delete(*listview.get_children())

                            for i, data in enumerate(records.values(), start=1):
                                # Get the user's attributes from the user object
                                surname = data['surname']
                                firstname = data['firstname']
                                username = data['username']
                                password = data['password']
                                account_type = data['account_type']

                                listview.insert("", "end", values=(i, surname, firstname, username, password, account_type))
                        except Exception as error:
                            print(error)
                            tkinter.messagebox.showerror('Error', 'Could not add the account')

                #Update function for mobile user
                def update():
                    id=a.get()
                    surname = a1.get()
                    firstname = a2.get()
                    username = a3.get()
                    password = a4.get()
                    account_type = listclass.get()

                    # Get a reference to the "mobile_user" node in your Firebase database
                    ref = db.reference('mobile_user')

                    try:
                        # Update the data in the Firebase database
                        ref.order_by_child('surname').equal_to(surname).update({
                            'firstname': firstname,
                            'username': username,
                            'password': password,
                            'account_type': account_type
                        })

                        tkinter.messagebox.showinfo("information", "Record updated successfully...")
                        a1.delete(0, END)
                        a2.delete(0, END)
                        a3.delete(0, END)
                        a4.delete(0, END)
                        listview.delete(*listview.get_children())
                        a1.focus_set()

                        # Update the Treeview after the database update
                        records = ref.get()
                        print(f"Updating records with surname {surname}")
                        print(records)
                        listview.delete(*listview.get_children())
                        for i, (id, data) in enumerate(records.items(), start=1):
                            listview.insert("", "end", values=(id, data['surname'], data['firstname'], data['username'], data['password'], data['account_type']))
                    except Exception as e:
                        print(e)
                        tkinter.messagebox.showerror("Error", "Record update failed.")

                #delete function for mobile_user
                def delete():
                    surname = a1.get()
                    if not surname:
                        tkinter.messagebox.showerror("Error", "No surname entered. Please enter a surname to delete.")
                        return
                    else:
                        # Connect to Firebase database
                        ref = db.reference('mobile_user')

                        try:
                            # Delete record from Firebase database
                            records = ref.order_by_child('surname').equal_to(surname).get()
                            if records:
                                record_key = list(records.keys())[0]
                                ref.child(record_key).delete()

                                tkinter.messagebox.showinfo("information", "Record deleted successfully...")
                                a.delete(0, END)
                                a1.delete(0, END)
                                a2.delete(0, END)
                                a3.delete(0, END)
                                a4.delete(0, END)
                                a1.focus_set()

                                # Update the Treeview after the database update
                                records = ref.get()
                                print(f"Deleting records with surname {surname}")
                                print(records)
                                listview.delete(*listview.get_children())
                                for i, record in enumerate(records.values(), start=1):
                                    listview.insert("", "end", values=(record['id'], record['surname'], record['firstname'], record['username'], record['password'], record['account_type']))
                            else:
                                tkinter.messagebox.showerror("Error", "No record found with that surname.")
                        except Exception as e:
                            print(e)

                #display the mobile user from database
                def show():
                    ref = db.reference('mobile_user')

                    # Retrieve all the records from the database
                    records = ref.get()

                    if records is None:
                        tkinter.messagebox.showinfo('Info', 'No records found')
                        return

                    # Clear the listview widget
                    listview.delete(*listview.get_children())

                    # Iterate over the records and insert them into the listview widget
                    for i, data in enumerate(records.values(), start=1):
                        listview.insert("", "end", values=(i, data['surname'], data['firstname'], data['username'], data['password'], data['account_type']))

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

                a3=tk.Label(bg, text='Username', font=('Inter', 14, 'bold'), fg='white', bg='#1151b8')
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

                cols = ('id','Surname', 'Firstname', 'Username', 'Password', 'Account_type')
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
                    elif col == 'Username':
                        listview.column(col, width=160)
                    elif col == 'Password':
                        listview.column(col, width=100)
                    else:
                        listview.column(col, width=180)
                    listview.grid(row=1, column=6, columnspan=1)
                    listview.place(x=0, y=0)
                show()

            def about_page():
                global about
                f1.destroy()

                about = ImageTk.PhotoImage(Image.open('image/about.png').resize(size=(900, 680)))

                f2=Frame(dash, width=1000, height=600, bg='#d8dee8')
                f2.place(x=0, y=40)
                l2=Label(dash, fg='#232323', font=('Inter', 18, 'bold'), bg='#d8dee8')
                l2.place(x=150, y=60)
                aboutimg = Label(f2, image=about, bg='#d8dee8')
                aboutimg.place(x=40, y=-70)


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

            home = tk.Button(f1, text='Home',border=0, fg='white', bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=dashboard_page)
            home.place(x=15, y=100)
            home.bind('<Enter>', on_enter)
            home.bind('<Leave>', on_leave)
           
            classroom = tk.Button(f1, text='Classrooms',border=0,fg='white' ,bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=classroom_page)
            classroom.place(x=15, y=150)
            classroom.bind('<Enter>', on_enter)
            classroom.bind('<Leave>', on_leave)

            account = tk.Button(f1, text='Accounts',border=0,fg='white' ,bg='#748299', width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=account_page)
            account.place(x=15, y=200)
            account.bind('<Enter>', on_enter)
            account.bind('<Leave>', on_leave)

            fa= tk.Button(f1, text='About',border=0, bg='#748299',fg='white' , width=20, font=('Inter', 16, 'bold'), cursor='hand2', command=about_page)
            fa.place(x=15, y=250)
            fa.bind('<Enter>', on_enter)
            fa.bind('<Leave>', on_leave)

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
        window_icon = ImageTk.PhotoImage(Image.open('image/bisu-logo.png'))
        dash.iconphoto(False, window_icon)


root = Tk()
mainframe = MainFrame(root)
root.mainloop()
