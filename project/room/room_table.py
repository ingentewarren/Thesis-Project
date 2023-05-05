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

        print(f"Room number for reservation in room {room_id}: {room_number}")

        if "Reserve" in room_data:
            reserve_data = room_data["Reserve"]
            reserve_ref = ref.child(room_id).child("Reserve")
            name = reserve_data.get("FullName")
            date = reserve_data.get("Date")
            event = reserve_data.get("Event")
            subject_code = reserve_data.get("SubjectCode")
            time_start = reserve_data.get("TimeStart")
            time_end = reserve_data.get("TimeEnd")

            if subject_code is None:
                print(f"Error: Subject code not found for room {room_number}")
                continue

            # Check if the reservation has started and hasn't ended yet
            now = datetime.now()
            start_time = datetime.strptime(time_start, "%H:%M")
            end_time = datetime.strptime(time_end, "%H:%M")
            if date == now.strftime("%m/%d/%Y") and start_time <= now <= end_time:
                # Insert the reservation data to the listview
                reservation = (name, date, room_number, event, subject_code, time_start, time_end)
                self.listview.insert("", "end", values=reservation)
            elif now < start_time:
                # Do nothing and wait for the reservation to start
                pass
            elif now > end_time:
                # Delete the reservation data from the database
                reserve_ref.delete()
                # Delete the reservation data from the listview
                for item in self.listview.get_children():
                    if self.listview.item(item)["values"][0] == name and \
                    self.listview.item(item)["values"][1] == date and \
                    self.listview.item(item)["values"][2] == room_number and \
                    self.listview.item(item)["values"][3] == event and \
                    self.listview.item(item)["values"][4] == subject_code and \
                    self.listview.item(item)["values"][5] == time_start and \
                    self.listview.item(item)["values"][6] == time_end:
                        self.listview.delete(item)
            else:
                # Insert the reservation data to the listview
                reservation = (name, date, room_number, event, subject_code, time_start, time_end)
                self.listview.insert("", "end", values=reservation)