import psycopg2

host = "heffalump.db.elephantsql.com"
user = 'sdjminza'
password = 'epNcEMj5bgVjhU8RNiVlWngeWDi6SwMR'
database = 'sdjminza'

def db_init():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # print(type(connection))
    if isinstance(connection,psycopg2.extensions.connection):
        print("db connected")
        cursor = connection.cursor()
    if isinstance(cursor,psycopg2.extensions.cursor):
        print("db initiation")

    return connection, cursor

def db_close(connection):
    connection.close()

connection, cusor = db_init()

db_close(connection)