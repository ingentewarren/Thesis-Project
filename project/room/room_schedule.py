import datetime
import mysql.connector

DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "localhost"
DB_port = "3306"

def add_schedule_event(start_datetime, end_datetime, room_id):
    # Connect to the database
    db = mysql.connector.connect(
        host = DB_hostname,
        user = DB_username,
        password = DB_password,
        database = DB_database, 
        port = DB_port
        )

    # Add the scheduled event to the database
    cursor = db.cursor()
    query = "INSERT INTO schedule (day, start_time, end_time, room_number) VALUES (%s, %s, %s, %s)"
    params = (start_datetime.strftime("%A"), start_datetime.time(), end_datetime.time(), room_id)
    try:
        cursor.execute(query, params)
        # Commit the changes and close the database connection
        db.commit()
        db.close()
        print("Schedule event added successfully.")
    except mysql.connector.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            print("Error: Schedule event already exists.")
        else:
            print("Error: Failed to add schedule event.")
        db.rollback()
        db.close()

def get_schedule(day):
    # Connect to the database
    db = mysql.connector.connect(
        host = DB_hostname,
        user = DB_username,
        password = DB_password,
        database = DB_database, 
        port = DB_port
    )

    # Query the schedule table for the given day
    cursor = db.cursor()
    query = "SELECT start_time, end_time, room_number FROM schedule WHERE day = %s"
    params = (day,)
    cursor.execute(query, params)
    result = cursor.fetchall()

    # Format the result as a list of tuples
    schedule = []
    for row in result:
        start_time = row[0].strftime("%H:%M:%S")
        end_time = row[1].strftime("%H:%M:%S")
        room_id = row[2]
        schedule.append((start_time, end_time, room_id))

    db.close()
    return schedule

def schedule_room_weekdays(start_time, end_time, room_id):
    # Create a list of weekdays to schedule
    weekdays = [0, 1, 2, 3, 4]  # Monday to Friday
    
    # Calculate the next occurrence of the scheduled time
    today = datetime.date.today()
    for i in range(7):
        date = today + datetime.timedelta(days=i)
        if date.weekday() in weekdays:
            # Combine the date with the start time
            start_datetime = datetime.datetime.combine(date, start_time)
            
            # Combine the date with the end time
            end_datetime = datetime.datetime.combine(date, end_time)
            
            # Add the scheduled event to the database
            add_schedule_event(start_datetime, end_datetime, room_id)

def schedule_room_custom(schedule_list):
    db = mysql.connector.connect(
        host = DB_hostname,
        user = DB_username,
        password = DB_password,
        database = DB_database, 
        port = DB_port
        )

    for schedule in schedule_list:
        day = schedule[0]
        start_time = schedule[1]
        end_time = schedule[2]
        room_id = schedule[3]
        
        # Calculate the next occurrence of the scheduled time
        today = datetime.date.today()
        for i in range(7):
            date = today + datetime.timedelta(days=i)
            if date.weekday() == day:
                # Combine the date with the start time
                start_datetime = datetime.datetime.combine(date, start_time)
                
                # Combine the date with the end time
                end_datetime = datetime.datetime.combine(date, end_time)
                
                # Add the scheduled event to the database
                cursor = db.cursor()
                query = "SELECT COUNT(*) FROM schedule WHERE day = %s AND start_time = %s AND end_time = %s AND room_number = %s"
                params = (day, start_datetime.time(), end_datetime.time(), room_id)
                cursor.execute(query, params)
                result = cursor.fetchone()
                
                # If the schedule doesn't exist, add it to the database
                if result[0] == 0:
                    add_schedule_event(start_datetime, end_datetime, room_id)

    # Close the database connection
    db.close()
#list of adding schedule in the room
schedule_list = [
    (0, datetime.time(9, 0), datetime.time(10, 0), 312),  # Monday, 9:00 AM to 10:00 AM
    (0, datetime.time(14, 0), datetime.time(15, 0), 312),  # Monday, 2:00 PM to 3:00 PM
    (1, datetime.time(9, 0), datetime.time(10, 0), 312),  # Monday, 9:00 AM to 10:00 AM
    (1, datetime.time(14, 0), datetime.time(15, 0), 312),
    (2, datetime.time(6, 47), datetime.time(7, 0), 311),
    (3, datetime.time(9, 0), datetime.time(10, 0), 311),  
    (4, datetime.time(14, 0), datetime.time(15, 0), 312),
]

schedule_room_custom(schedule_list)

