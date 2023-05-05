from tkinter import *
import tkinter as tk
from tkinter import ttk, END
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

class room_available_window:
    def __init__(self, available):
        super().__init__()
        self.available = available
        self.available.title("Room Available")
        self.available.geometry("700x500")
        self.available.resizable(False, False)

        Label(self.available, text='Room Available', font=('Inter', 24, 'bold'), fg='#2B3467').place(x=20, y=20)

        cols = ('Room #', 'Department', 'Room Location', 'status')
        listview = ttk.Treeview(self.available, columns=cols, show='headings', height=18)

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
            availability = room_data.get('Availability', True)
            status = "Available" if availability else "Not Available"
            
            if availability:
                self.listview.insert("", "end", values=(room_number, department, location, status))

if __name__ == '__main__':
    root = Tk()
    available_window = room_available_window(root)
    root.mainloop()