import psycopg2

def db_connect():
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def db_close(self):
    if self is not None:
        self.close()
        print('Database connection closed.')


if __name__ == '__main__':
#    conn = dbhelper.db_connect()
    conn = db_connect()
#    dbhelper.db_close(conn)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM swtypes')
    records = cursor.fetchall()
#    print(records)

#    for i in records:
#        print(i)

    for i in range(len(records)):
        print("User " + str(records[i]))
#    db_close(conn)
