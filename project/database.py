import psycopg2
import psycopg2.extras

DB_database = "postgres"
DB_username = "postgres"
DB_password = "entercore123"
DB_hostname = "localhost"
DB_port = "5432"
conn = None
cur = None
try:
    conn = psycopg2.connect(
        host = DB_hostname,
        user = DB_username,
        password = DB_password,
        dbname = DB_database,
        port = DB_port
        )
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DROP TABLE IF EXISTS users")
    
    create_script = '''CREATE TABLE IF NOT EXISTS users (
                            id int PRIMARY KEY,
                            name varchar(100) NOT NULL,
                            password varchar(100) NOT NULL,
                            username varchar(100) NOT NULL,
                            email varchar(100) NOT NULL
    )'''
    cur.execute(create_script)

    insert_script = 'INSERT INTO users (id, name, password, username, email) VALUES (%s, %s, %s, %s, %s)'
    insert_values = [(1, 'warren', 'admin', 'warrenikaw1', 'ingentewarren1@gmail.com'), 
                     (2, 'warren', 'admin', 'warrenikaw1', 'ingentewarren1@gmail.com'),
                     (3, 'warren', 'admin', 'warrenikaw1', 'ingentewarren1@gmail.com'),
                     (4, 'warren', 'admin', 'warrenikaw1', 'ingentewarren1@gmail.com'),
                     (5, 'warren', 'admin', 'warrenikaw1', 'ingentewarren1@gmail.com'),]
  
    for record in insert_values:
        cur.execute(insert_script, record)

    cur.execute('SELECT * FROM users')
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