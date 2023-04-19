from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import mysql.connector  
import datetime


DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "localhost"
DB_port = "3306"

class room_install:
    def __init__(self, install):
        super().__init__()
        self.install = install
        self.install.title("Add room")
        self.install.geometry("400x550")
        self.install.resizable(False, False)

        global listclass
        
        Label(self.install, text="ADD ROOM", font=('Inter', 20, 'bold'), fg='#2B3467').place(x=120, y=10)
        Label(self.install, text="Room #: ").place(x=45, y=50)
        Label(self.install, text="Department: ").place(x=45, y=100)
        Label(self.install, text="Room Location: ").place(x=45, y=150)

        self.room_number_entry = Entry(self.install, width=50)
        self.department_entry = Entry(self.install, width=50)
        self.location_entry = Entry(self.install, width=50)

        department_lists = ['Engineering, Architecture & Industrial Design', 'Business Arts & Sciences', 'Technology & Allied Sciences', 'Teacher Education']
        listclass = StringVar(self.install)
        listclass.set("College of : ")
        self.department_entry = OptionMenu(self.install, listclass, *department_lists)

        self.room_number_entry.place(x=45, y=70)
        self.department_entry.place(x=45, y=120, width=310)
        self.location_entry.place(x=45, y=180)

        # Create submit button
        submit_button = Button(self.install, text="Submit", command=self.submit, width=20, border=0, bg='#2B3467', fg='white', font=("inter", 12, 'bold'))
        submit_button.place(x=95, y=500)

    def submit(self):
    
        room_number = self.room_number_entry.get()
        department = listclass.get()
        location = self.location_entry.get()

        # Save reservation data to a file or database
        if not room_number or not room_number.isdigit():
            tkinter.messagebox.showerror('Error', 'Please enter room number')
        else:
            try:
                int(self.room_number_entry.get())
            except ValueError:
                tkinter.messagebox.showerror('error', 'The room number should be integers')
        
        if department == 'College of : ':
            tkinter.messagebox.showerror('Error', 'Please select a department')

        if location == '':
            tkinter.messagebox.showerror('Error', 'Please enter location') 

        if room_number != '' and department != '' and location != '':
            tkinter.messagebox.showinfo('', 'Adding account success')
            self.install.destroy()

            conn = mysql.connector.connect(
                host = DB_hostname,
                user = DB_username,
                password = DB_password,
                database = DB_database,
                port = DB_port
                )
            mycursor=conn.cursor()

            try:
                mycursor.execute("INSERT INTO room ( room_number, department, location) VALUES ( %s, %s, %s) ",
                        (room_number, department, location))
                conn.commit()
                self.room_number_entry.delete(0, END)
                self.department_entry.delete(0, END)
                self.location_entry.delete(0, END)
                self.room_number_entry.focus_set()
             
                # Update the listview with the added room data
                room_data = f"Room No.: {room_number}, Department: {department}, Location: {location}"
                self.listview.insert(END, room_data)
                
            except mysql.connector.Error as error:
                print(error)
                tkinter.messagebox.showerror('Error', 'Could not add the room')
            finally:
                conn.rollback()
            conn.close()

class room_info_window:
    def __init__(self, room_info):
        super().__init__()
        self.room_info = room_info
        self.room_info.title("Room Information")
        self.room_info.configure(bg='#d8dee8')
        self.room_info.geometry("400x550")
        self.room_info.resizable(False, False)

        def room_information():
            room_num = StringVar()
            department = StringVar()
            location = StringVar()
            status = StringVar()

            conn = mysql.connector.connect(
                host = DB_hostname,
                user = DB_username,
                password = DB_password,
                database = DB_database,
                port = DB_port
                )
            mycursor=conn.cursor()

            options = []
            query = "SELECT room_number FROM room"
            mycursor.execute(query)
            result = mycursor.fetchall()
            for i in result:
                options.append(str(i[0]))

            def lookup_room(event):
                mydb = mysql.connector.connect(
                    host = DB_hostname,
                    user = DB_username,
                    password = DB_password,
                    database = DB_database,
                    port = DB_port
                )
                mycursor = mydb.cursor()

                option = room_list.get()
                cid = option.split(',')[0]
                query = "SELECT * FROM room WHERE room_number = %s"
                mycursor.execute(query, (cid,))
                row = mycursor.fetchone()
                for i in row:
                    room_num.set(row[1])
                    department.set(row[2])
                    location.set(row[3])
                    status.set(row[4])

            opts = StringVar()
            Label(self.room_info, text='Room Information', fg='#2B3467', font=('Inter', 24, 'bold'), bg='#d8dee8').place(x=50, y=20)
            Label(self.room_info, textvariable=opts, font=('Inter',12, 'bold'), fg='#2B3467', bg='#d8dee8').place(x=135   , y=70)
            Label(self.room_info, text="Room Number: ", font=('Inter', 11, 'bold'), fg='#2B3467', bg='#d8dee8').place(x=20, y=70)

            room_list = ttk.Combobox(self.room_info, textvariable=opts, width=55)
            room_list['values'] = options
            room_list.place(x=20, y=95)
            room_list.current(0)
            room_list.bind("<<ComboboxSelected>>", lookup_room)


            wrapper_frame = Frame(self.room_info, width=351, height=355, bg='#d8dee8')
            wrapper_frame.place(x=20, y=130)
            room_info_wrapper = Label(wrapper_frame, text='Room Information', font=('arial', 11, 'bold'), fg='#2B3467', bg='#d8dee8')
            room_info_wrapper.place(x=0, y=0)

            Label(wrapper_frame, text='Room #: ', bg='#d8dee8', fg='#2B3467', font=('arial', 10, 'bold')).place(x=0, y=30)
            Label(wrapper_frame, text='Department: ', bg='#d8dee8', fg='#2B3467', font=('arial', 10, 'bold')).place(x=0, y=60)
            Label(wrapper_frame, text='Location: ', bg='#d8dee8', fg='#2B3467', font=('arial', 10, 'bold')).place(x=0, y=90)
            Label(wrapper_frame, text='Status: ', bg='#d8dee8', fg='#2B3467', font=('arial', 10, 'bold')).place(x=0, y=120)

            Entry(wrapper_frame, width=50, border=0, bg='#d8dee8', textvariable=room_num, fg='#2B3467', font=('arial', 10, 'bold')).place(x=100, y=30)
            Entry(wrapper_frame, width=50, border=0, bg='#d8dee8', textvariable=department, fg='#2B3467', font=('arial', 10, 'bold')).place(x=100, y=60)
            Entry(wrapper_frame, width=50, border=0, bg='#d8dee8', textvariable=location, fg='#2B3467', font=('arial', 10, 'bold')).place(x=100, y=90)
            Entry(wrapper_frame, width=50, border=0, bg='#d8dee8', textvariable=status, fg='#2B3467', font=('arial', 10, 'bold')).place(x=100, y=120)

        room_information()

class room_installed_window:
    def __init__(self, master):
        self.master = master
        master.title('ROOM INSTALLED')
        master.geometry('700x500')
        master.resizable(False, False)

        room_installed_screen = Frame(master, width=690, height= 490, bg='#d8dee8')
        room_installed_screen.place(x=5, y=5)
        add_room_buttom = Button(room_installed_screen, width=20, text='Add Room', command=self.add_room, bg='#2B3467', border=0, font=("inter", 12, "bold"), fg='white')
        add_room_buttom.place(x=20, y=20)
        room_info_button = Button(room_installed_screen, width=20, text='Room Information', command=self.show_room_info, bg='#2B3467', border=0, font=("inter", 12, "bold"), fg='white')
        room_info_button.place(x=465, y=20)

        cols = ('Room #', 'Department', 'Room Location', 'status')
        listview = ttk.Treeview(self.master, columns=cols, show='headings', height=18)

        for col in cols:
                listview.heading(col, text=col)
                if col == 'room #':
                    listview.column(col, width=10)
                elif col == 'department':
                    listview.column(col, width=40)
                elif col == 'Room Location':
                    listview.column(col, width=250)
                else:
                    listview.column(col, width=135)
                listview.grid(row=1, column=5, columnspan=1)
                listview.place(x=20, y=100)

        self.listview = listview
        self.populate_listview()

    def populate_listview(self):
        conn = mysql.connector.connect(
            host=DB_hostname,
            user=DB_username,
            password=DB_password,
            database=DB_database,
            port=DB_port
        )
        mycursor = conn.cursor()

        mycursor.execute("SELECT room_number, department, location, status FROM room")
        records = mycursor.fetchall()

        for row in records:
            is_booked = self.is_booked(row[0])
            if is_booked:
                status = 'occupied'
            else:
                status = 'available'
            
            query = "UPDATE room SET status = %s WHERE room_number = %s"
            values = (status, row[0])
            mycursor.execute(query, values)
            conn.commit()

            self.listview.insert("", "end", values=(row[0], row[1], row[2], status, ''))

        conn.close()

    def update_room_status(self, room_number, status):
        conn = mysql.connector.connect(
            host=DB_hostname,
            user=DB_username,
            password=DB_password,
            database=DB_database,
            port=DB_port
        )
        mycursor = conn.cursor()

        # Update the status of the room in the room table
        try:
            mycursor.execute("UPDATE room SET status = %s WHERE room_number = %s", (status, room_number))
            conn.commit()
            print("Room status updated")
        except mysql.connector.Error as error:
            print(error)
        print("Could not update room status")

        conn.close()

    def is_booked(self, room_number):
        conn = mysql.connector.connect(
            host=DB_hostname,
            user=DB_username,
            password=DB_password,
            database=DB_database,
            port=DB_port
        )
        mycursor = conn.cursor()

        query = "SELECT * FROM reservation WHERE room_number = %s"
        values = (room_number,)
        mycursor.execute(query, values)
        result = mycursor.fetchone()

        conn.close()

        if result is not None and result[0]>0:
            return True
        else:
            return False
        
    def is_room_available(self, room_number):
        scheduled = self.is_room_scheduled(room_number)
        occupied = self.is_booked(room_number)
        anyone_in_room = self.is_anyone_in_room()

        # Return True if room is available, otherwise False
        if not scheduled and not occupied and not anyone_in_room:
            return True
        else:
            return False
        
    def is_room_scheduled(self, room_number):
        # Your existing is_room_scheduled() function code
            # Connect to the database
        db = mysql.connector.connect(
            host = DB_hostname,
            user = DB_username,
            password = DB_password,
            database = DB_database, 
            port = DB_port
        )

        # Query the schedule table for the given room number
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM schedule WHERE room_number = %s"
        params = (room_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        # Extract the count from the result
        count = result[0]

        # Close the database connection
        db.close()

        # If count is greater than 0, then room is scheduled, else not scheduled
        return count > 0

    def add_room(self):
        room_window = Toplevel(self.master)
        room_install(room_window)

    def show_room_info(self):
        room_info_window1 = Toplevel(self.master)
        room_info_window(room_info_window1)
        

if __name__ == '__main__':
    root = Tk()
    installed_window = room_installed_window(root)
    root.mainloop()