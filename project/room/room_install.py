from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image  
from datetime import datetime
from tkinter import messagebox, END
import datetime, time
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

class room_install:
    def __init__(self, install):
        super().__init__()
        self.install = install
        self.install.title("Add room")
        self.install.geometry("400x350")
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
        submit_button.place(x=95, y=300)

        window_icon = ImageTk.PhotoImage(Image.open('image/bisu-logo.png'))
        self.install.iconphoto(False, window_icon)

    def submit(self):
        room_number = self.room_number_entry.get()
        department = listclass.get()
        location = self.location_entry.get()

        if not room_number or not room_number.isdigit():
            tkinter.messagebox.showerror('Error', 'Please enter room number')
            return
        else:
            room_number = int(room_number)

        if department == 'College of : ':
            tkinter.messagebox.showerror('Error', 'Please select a department')
            return

        if location == '':
            tkinter.messagebox.showerror('Error', 'Please enter location')
            return

        try:

            ref = db.reference('Room')
            if ref.get() is None:  
                ref.set({}) 


            num_rooms = len(ref.get()) if ref.get() else 0
            new_room_key = f"Room{num_rooms + 1}"
            new_room_ref = ref.child(new_room_key)
            new_room_ref.set({
                'Room Number': room_number,
                'department': department,
                'location': location,
                'Availability': True,
            })
            tkinter.messagebox.showinfo('', 'Adding account success')
            self.install.destroy()

            room_data = f"Room No.: {room_number}, Department: {department}, Location: {location}"
        
        except Exception as e:
            print(e)
            
class room_info_window:
    def __init__(self, room_info):
        super().__init__()
        self.room_info = room_info
        self.room_info.title("Room Information")
        self.room_info.configure(bg='#d8dee8')
        self.room_info.geometry("400x550")
        self.room_info.resizable(False, False)

        room_num = StringVar()
        department = StringVar()
        location = StringVar()
        status = StringVar()

        try:
            rooms = db.reference("Room").get()
            options = []

            for room_key, room_data in rooms.items():
                options.append(room_data["Room Number"])

            option_var = StringVar()
            option_var.set(options[0])
            option_menu = OptionMenu(root, option_var, *options)
            option_menu.pack()
            def lookup_room(*args):
                option = option_var.get()
                if option == "":
                    # Clear the room information and schedule label when no room is selected
                    room_num.set("")
                    department.set("")
                    location.set("")
                    status.set("")
                    schedule_label.config(text="")
                    return

                try:
                    room_data = rooms[option]
                    room_num.set(room_data['Room Number'])
                    department.set(room_data['Department'])
                    location.set(room_data['Location'])
                    status.set(room_data['Availability'])

                    schedule_data = room_data.get('Schedule', {})
                    schedule_label.config(text="")
                    if schedule_data:
                        schedule_str = "Schedule:\n"
                        for day, slots in schedule_data.items():
                            schedule_str += f"{day.capitalize()}\n"
                            for slot_key, slot_data in slots.items():
                                schedule_str += f"- {slot_key}: {slot_data['time_start']} - {slot_data['time_end']}\n"
                        schedule_label.config(text=schedule_str)
                    else:
                        schedule_label.config(text="No schedule found for this room.")  # Update schedule label when no schedule found
                except Exception as e:
                    print("Error: ", e)

            option_var.trace("w", lookup_room)

            Label(self.room_info, text='Room Information', fg='#2B3467', font=('Inter', 24, 'bold'), bg='#d8dee8').place(x=50, y=20)
            Label(self.room_info, text="Room Number: ", font=('Inter', 11, 'bold'), fg='#2B3467', bg='#d8dee8').place(x=20, y=70)

            room_list = ttk.Combobox(self.room_info, width=55, values=options)
            room_list.place(x=20, y=95)
            room_list.current(0)
            room_list.bind("<<ComboboxSelected>>", lookup_room)

            wrapper_frame = Frame(self.room_info, width=351, height=500, bg='#d8dee8')
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

            schedule_label = Label(wrapper_frame, text=" ", wraplength=350, justify=LEFT, font=('arial', 10, 'bold'), bg='#d8dee8', fg='#2B3467')
            schedule_label.place(x=0, y=150)

        except Exception as e:
            print("Error", e)

        window_icon = ImageTk.PhotoImage(Image.open('image/bisu-logo.png'))
        self.room_info.iconphoto(False, window_icon)
      
        

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
                    listview.column(col, width=50)
                elif col == 'Room Location':
                    listview.column(col, width=250)
                else:
                    listview.column(col, width=135)
                listview.grid(row=1, column=5, columnspan=1)
                listview.place(x=20, y=100)

        self.listview = listview
        self.populate_listview()
        window_icon = ImageTk.PhotoImage(Image.open('image/bisu-logo.png'))
        master.iconphoto(False, window_icon)


    def populate_listview(self):
        ref = db.reference('Room')
        rooms_snapshot = ref.get()

        if not rooms_snapshot:
            print("Error: Unable to retrieve rooms data from the database")
            return

        if not isinstance(rooms_snapshot, dict):
            print("Error: Rooms data is not in the expected format")
            return

        for room_id, room_data in rooms_snapshot.items():
            if not isinstance(room_data, dict):
                print(f"Error: Room data for room {room_id} is not in the expected format")
                continue

            room_number = room_data.get('Room Number', '')
            department = room_data.get('department', '')
            location = room_data.get('location', '')
            availability = room_data.get('Availability', '')

            if self.is_reserved(room_id):
                status = "Occupied"
            elif self.get_scheduled_rooms(room_id):
                status = "Scheduled"
            else:
                status = "Vacant"
         

            # Only update the availability value in the database if it has changed
            if room_data.get('Availability', None) != availability:
                room_data.update({'Availability': availability})
                room_ref = db.reference(f"Room/{room_id}")
                room_ref.update(room_data)

            self.listview.insert("", "end", values=(room_number, department, location, status))


    def is_reserved(self, room_id):
        room_ref = db.reference(f"Room/{room_id}")
        reserve_data = room_ref.child("Reserve").get()

        if reserve_data is None:
            return False

        if not isinstance(reserve_data, dict):
            print(f"Error: Reserve data for room {room_id} is not in the expected format")
            return False
        
        time_start = reserve_data.get("TimeStart")
        if time_start is None:
            print(f"Error: TimeStart value not found for room {room_id}")
            return False
        
        current_time = datetime.now().strftime('%H:%M')
        if current_time >= time_start:
            return True
        
        return False
        
    def get_scheduled_rooms(self, room_id):
        current_time = datetime.now()
        current_day = current_time.strftime('%A')
        current_time_str = current_time.strftime('%H:%M')

        room_ref = db.reference(f"Room/{room_id}")
        room_schedule = room_ref.child('Schedule').get()

        if room_schedule is None or current_day not in room_schedule:
            return None

        day_schedule = room_schedule[current_day]
        if not day_schedule:
            return None

        for i in range(1, 4):
            start_time = day_schedule.get(f"time_start{i}")
            end_time = day_schedule.get(f"time_end{i}")

            if start_time and end_time:
                if current_time_str >= start_time and current_time_str < end_time:
                    return True
        return False

    def add_room(self):
        room_window = Toplevel(self.master)
        self.room_install_obj = room_install(room_window)
        room_window.wait_window(self.room_install_obj.install)
        
        self.listview.delete(*self.listview.get_children())
        self.populate_listview()

        start_time = time.time()
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000

        print(f'Data written in {elapsed_time_ms} milliseconds.')

    def show_room_info(self):
        room_info_window1 = Toplevel(self.master)
        room_info_window(room_info_window1)


if __name__ == '__main__':
    root = Tk()
    installed_window = room_installed_window(root)
    root.mainloop()
    