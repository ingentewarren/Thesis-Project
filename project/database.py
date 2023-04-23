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
    cur.execute("DROP TABLE IF EXISTS admin_user")
    
    create_script = '''CREATE TABLE IF NOT EXISTS admin_user (
                            id int PRIMARY KEY,
                            username varchar(100) NOT NULL,
                            password varchar(100) NOT NULL,
                            name varchar(100) NOT NULL
    )'''
    cur.execute(create_script)

    insert_script = 'INSERT INTO admin_user (id, username, password, name) VALUES (%s, %s, %s, %s)'
    insert_values = [(1, 'admin', 'admin', 'warren ingente'), 
                     (2, 'admin1', 'admin', 'warren'),
                     (3, 'admin2', 'admin', 'war2')]
  
    for record in insert_values:
        cur.execute(insert_script, record)

    cur.execute('SELECT * FROM admin_user')
    for record in cur.fetchall():
        print(record['id'], record['name'])

    conn.commit()
except Exception as error:
    print(error)   
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()