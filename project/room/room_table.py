import mysql.connector


DB_database = "admin"
DB_username = "root"
DB_password = "entercore123"
DB_hostname = "192.168.254.113"
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
    cur.execute("DROP TABLE IF EXISTS room")
    
    create_script = '''CREATE TABLE IF NOT EXISTS room (
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            room_number INT NOT NULL,
                            department varchar(100) NOT NULL,
                            location varchar(100) NOT NULL
                        )'''
    cur.execute(create_script)

    alter_script = '''ALTER TABLE room ADD status VARCHAR(255)'''
    cur.execute(alter_script)

    cur.execute('SELECT * FROM room')
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