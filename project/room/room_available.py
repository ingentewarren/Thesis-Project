from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import mysql.connector  


DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "localhost"
DB_port = "3306"

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
            listview.heading(col, text=col, anchor='center')
            if col == 'room #':
                listview.column(col, width=10)
            elif col == 'department':
                listview.column(col, width=40)
            elif col == 'Room Location':
                listview.column(col, width=250)
            elif col == 'status':
                listview.column(col, width=100)
            else:
                listview.column(col, width=100)
            listview.grid(row=1, column=5, columnspan=1)
            listview.place(x=20, y=80)
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

        mycursor.execute("SELECT room_number, department, location, status FROM room WHERE status ='available'")
        records = mycursor.fetchall()

        for row in records:
            self.listview.insert("", "end", values=row)
        conn.close()


if __name__ == '__main__':
    root = Tk()
    available_window = room_available_window(root)
    root.mainloop()