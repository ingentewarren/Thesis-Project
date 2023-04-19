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


class room_info_window:
    def __init__(self, room_info):
        super().__init__()
        self.room_info = room_info
        self.room_info.title("Room Information")
        self.room_info.geometry("400x550")
        self.room_info.resizable(False, False)

        def room_number():
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
        
            opts = StringVar()
            Label(self.room_info, text='Room Information', fg='#2B3467', font=('Inter', 24, 'bold')).place(x=50, y=20)
            Label(self.room_info, textvariable=opts, font=('Inter',12, 'bold'), fg='#2B3467').place(x=135   , y=70)
            Label(self.room_info, text="Room Number: ", font=('Inter', 11, 'bold'), fg='#2B3467').place(x=20, y=70)

            room_list = ttk.Combobox(self.room_info, textvariable=opts, width=55)
            room_list['values'] = options
            room_list.place(x=20, y=95)

        room_number()
        room_info_wrapper = Label(self.room_info, text='Room Information')

if __name__ == '__main__':
    root = Tk()
    room_information_window = room_info_window(root)
    root.mainloop()