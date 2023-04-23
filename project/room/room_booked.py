from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import mysql.connector  


DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "192.168.254.113"
DB_port = "3306"

class room_occupied_window:
    def __init__(self, occupied):
        super().__init__()
        self.occupied = occupied
        self.occupied.title("Room Occupied")
        self.occupied.geometry("700x500")
        self.occupied.resizable(False, False)

        Label(self.occupied, text='Room Booked', font=('Inter', 24, 'bold'), fg='#2B3467').place(x=20, y=20)

        cols = ('Room #', 'Department', 'Room Location', 'status')
        listview = ttk.Treeview(self.occupied, columns=cols, show='headings', height=18)

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

        mycursor.execute("SELECT room_number, department, location, status FROM room WHERE status ='occupied'")
        records = mycursor.fetchall()

        for row in records:
            self.listview.insert("", "end", values=row)
        conn.close()


if __name__ == '__main__':
    root = Tk()
    occupied_window = room_occupied_window(root)
    root.mainloop()