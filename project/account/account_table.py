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
    cur.execute("DROP TABLE IF EXISTS mobile_user")
    
    create_script = '''CREATE TABLE IF NOT EXISTS mobile_user (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            surname varchar(100) NOT NULL,
                            firstname varchar(100) NOT NULL,
                            username varchar(100) NOT NULL,
                            password varchar(100) NOT NULL,
                            account_type varchar(20) NOT NULL
                        )'''
    cur.execute(create_script)

    cur.execute('SELECT * FROM mobile_user')
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