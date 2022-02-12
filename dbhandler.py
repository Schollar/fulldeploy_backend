import dbcreds
import mariadb as db


def db_connect():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print('Something is wrong with the DB')
    except:
        print('Something went wrong connecting to the DB')
    return conn, cursor
# Disconnect function that takes in the conn and cursor and attempts to close both


def db_disconnect(conn, cursor):
    try:
        cursor.close()
    except:
        print('Error closing cursor')
    try:
        conn.close()
    except:
        print('Error closing connection')

# Get posts function gets the jokes from the DB and returns them.


def get_jokes():
    success = False
    jokes = []
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "SELECT id, content FROM joke")
        jokes = cursor.fetchall()
        success = True
    except db.OperationalError:
        print('Something is wrong with the db!')
    except db.ProgrammingError:
        print('Error running DB query')
    except:
        print('Error with the DB')
    db_disconnect(conn, cursor)

    return success, jokes


def add_post(content):
    success = False
    conn, cursor = db_connect()
    try:
        cursor.execute(
            "INSERT INTO joke (content) VALUES (?)", [content])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except db.OperationalError:
        print('Something is wrong with the db!')
    except db.ProgrammingError:

        print('Error running DB query')
    db_disconnect(conn, cursor)
    success = True
    return success
