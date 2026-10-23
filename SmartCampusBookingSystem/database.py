import sqlite3

DB_NAME = "campus_booking.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_id TEXT UNIQUE,
        resource_name TEXT,
        campus TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        campus TEXT,
        resource_id TEXT,
        booking_date TEXT,
        start_time TEXT,
        duration INTEGER
    )
    """)

    conn.commit()
    conn.close()


def register_user(username, password, role):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users
        (username,password,role)
        VALUES(?,?,?)
        """, (username, password, role))

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()


def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role
    FROM users
    WHERE username=?
    AND password=?
    """, (username, password))

    result = cursor.fetchone()

    conn.close()

    return result

def add_resource(resource_id, resource_name, campus):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO resources
        (resource_id, resource_name, campus)
        VALUES(?,?,?)
        """, (
            resource_id,
            resource_name,
            campus
        ))

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()


def get_resources(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resources
    WHERE campus=?
    """, (campus,))

    resources = cursor.fetchall()

    conn.close()

    return resources

def create_booking(
    username,
    campus,
    resource_id,
    booking_date,
    start_time,
    duration
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM bookings
    WHERE resource_id=?
    AND booking_date=?
    AND start_time=?
    """, (
        resource_id,
        booking_date,
        start_time
    ))

    overlap = cursor.fetchone()

    if overlap:

        conn.close()
        return False

    cursor.execute("""
    INSERT INTO bookings
    (
        username,
        campus,
        resource_id,
        booking_date,
        start_time,
        duration
    )
    VALUES(?,?,?,?,?,?)
    """, (
        username,
        campus,
        resource_id,
        booking_date,
        start_time,
        duration
    ))

    conn.commit()
    conn.close()

    return True

def get_resources(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_id
    FROM resources
    WHERE campus=?
    """, (campus,))

    resources = cursor.fetchall()

    conn.close()

    return resources

def get_user_bookings(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,
           campus,
           resource_id,
           booking_date,
           start_time,
           duration
    FROM bookings
    WHERE username=?
    """, (username,))

    bookings = cursor.fetchall()

    conn.close()

    return bookings

def cancel_booking(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id=?
    """, (booking_id,))

    conn.commit()
    conn.close()

    return True

def get_all_resources():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_id,
           resource_name,
           campus
    FROM resources
    """)

    resources = cursor.fetchall()

    conn.close()

    return resources

def delete_resource(resource_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM resources
    WHERE resource_id=?
    """, (resource_id,))

    conn.commit()
    conn.close()

def get_all_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT campus,
           resource_id,
           booking_date,
           duration
    FROM bookings
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_total_bookings_per_campus():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT campus,
           COUNT(*)
    FROM bookings
    GROUP BY campus
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_most_used_resources():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_id,
           COUNT(*)
    FROM bookings
    GROUP BY resource_id
    ORDER BY COUNT(*) DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_average_duration():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(duration)
    FROM bookings
    """)

    data = cursor.fetchone()

    conn.close()

    return data

def get_booking_rule(campus):

    rules = {
        "Johannesburg": 4,
        "Pretoria": 3,
        "Durban": 2
    }

    return rules.get(campus, 1)

def get_campus_bookings(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username,
           resource_id,
           booking_date,
           start_time,
           duration
    FROM bookings
    WHERE campus = ?
    """, (campus,))

    bookings = cursor.fetchall()

    conn.close()

    return bookings

def update_resource(
    resource_id,
    new_name
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE resources
    SET resource_name = ?
    WHERE resource_id = ?
    """, (
        new_name,
        resource_id
    ))

    conn.commit()

    conn.close()

def get_available_resources(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_id
    FROM resources
    WHERE campus = ?
    """, (campus,))

    all_resources = cursor.fetchall()

    cursor.execute("""
    SELECT DISTINCT resource_id
    FROM bookings
    WHERE campus = ?
    """, (campus,))

    booked_resources = cursor.fetchall()

    conn.close()

    all_set = set()

    for resource in all_resources:
        all_set.add(resource[0])

    booked_set = set()

    for resource in booked_resources:
        booked_set.add(resource[0])

    available = all_set - booked_set

    return list(available)

def get_resource_usage_by_campus(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_id,
           COUNT(*)
    FROM bookings
    WHERE campus = ?
    GROUP BY resource_id
    ORDER BY COUNT(*) DESC
    """, (campus,))

    data = cursor.fetchall()

    conn.close()

    return data

def get_total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM users
    """)

    result = cursor.fetchone()

    conn.close()

    return result[0]

def get_total_resources():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM resources
    """)

    result = cursor.fetchone()

    conn.close()

    return result[0]

def get_total_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    """)

    result = cursor.fetchone()

    conn.close()

    return result[0]