import psycopg2


def db_connect():
    try:
        conn = psycopg2.connect(host="localhost",
                                database="sanenv",
                                user="admin",
                                password="postgres")
        print('Database connection opened.')
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR: ' + str(error))

    return conn


def db_insert(sql, var=''):
    conn = db_connect()
    with conn:
        with conn.cursor() as cursor:
            try:
                #cursor.execute(sql, var)
                cursor.execute(sql)
                switch_id = cursor.fetchone()[0]
            except (Exception,  psycopg2.DatabaseError) as error:
                print('ERROR: ' + str(error) + '\nSQL: ' + str(sql))
            finally:
                print('Database connection closed.')

    return switch_id


def db_select(sql):
    conn = db_connect()
    with conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
            except (Exception, psycopg2.DatabaseError) as error:
                print('ERROR: ' + str(error))
            finally:
                print('Database connection closed.')

        return result


if __name__ == '__main__':
#    conn = dbhelper.db_connect()
#    conn = db_connect()
#    dbhelper.db_close(conn)
#    cursor = conn.cursor()

#    cursor.execute('SELECT * FROM swtypes')
#    records = cursor.fetchall()
#    print(records)

#    for i in records:
#        print(i)

#    sql = 'SELECT * FROM swtypes'
    result = db_select('SELECT * FROM swtypes')

    for i in range(len(result)):
        print("User " + str(result[i]))