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
    cur.execute("DROP TABLE IF EXISTS schedule")
    
    create_script = '''CREATE TABLE IF NOT EXISTS schedule (
                            id INT NOT NULL AUTO_INCREMENT,
                            day VARCHAR(10) NOT NULL,
                            start_time TIME NOT NULL,
                            end_time TIME NOT NULL,
                            room_number INT NOT NULL,
                            PRIMARY KEY (id)
                        )'''
    cur.execute(create_script)

    cur.execute('SELECT * FROM schedule')
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