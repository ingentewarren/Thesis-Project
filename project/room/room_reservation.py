import mysql.connector


DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "192.168.79.2"
DB_port = "3306"
conn = None
cur = None
try:
    conn = mysql.connector.connect(
        host = DB_hostname,
        user = DB_username,
        password = DB_password,
        database = DB_database, 
        port = DB_port
        )
    
    cur = conn.cursor(dictionary=True)
    cur.execute("DROP TABLE IF EXISTS reservation")
    
    create_reservation_script = '''CREATE TABLE IF NOT EXISTS reservation (
                        id INT AUTO_INCREMENT,
                        name VARCHAR(255),
                        account_Type VARCHAR(255),
                        room_number INT NOT NULL,
                        event VARCHAR(255),
                        subject_Code VARCHAR(255),
                        time_Start TIME,
                        time_End TIME,
                        PRIMARY KEY (id)
                        )'''
    
    create_booked_script = '''CREATE TABLE IF NOT EXISTS booked (
                        id INT AUTO_INCREMENT,
                        reservation_id INT,
                        PRIMARY KEY (id),
                        FOREIGN KEY (reservation_id) REFERENCES reservation(id)
                        )'''
    
    create_reservation_history = '''CREATE TABLE IF NOT EXISTS reservation_history (
                        id INT AUTO_INCREMENT,
                        name VARCHAR(255),
                        account_Type VARCHAR(255),
                        room_number INT NOT NULL,
                        event VARCHAR(255),
                        subject_Code VARCHAR(255),
                        time_Start TIME,
                        time_End TIME,
                        reservation_date DATE,
                        reservation_time TIME,
                        PRIMARY KEY (id)
                        );'''
    cur.execute(create_reservation_script)
    cur.execute(create_booked_script) 
    cur.execute(create_reservation_history) 

    cur.execute('SELECT * FROM reservation')
    for record in cur.fetchall():
        print(record('id'), record('email'))

    conn.commit()
except Exception as error:
    print(error)   
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()