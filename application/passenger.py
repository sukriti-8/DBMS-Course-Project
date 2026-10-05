from application.database import fetch_all, fetch_one, execute_query

def get_all_passengers():
    """Retrieve all passenger records from the database."""
    query = "SELECT * FROM Passenger ORDER BY passenger_id DESC"
    return fetch_all(query)

def get_passenger_by_id(passenger_id):
    """Retrieve a single passenger record by ID."""
    query = "SELECT * FROM Passenger WHERE passenger_id = %s"
    return fetch_one(query, (passenger_id,))

def add_passenger(name, email, phone, passport_no):
<<<<<<< Updated upstream
    """Insert a new passenger record into the database."""
    query = """
        INSERT INTO Passenger (name, email, phone, passport_no)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (name.strip(), email.strip(), phone.strip(), passport_no.strip()))
=======
    if not name or not email or not phone or not passport_no:
        print("All passenger details are required.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO Passenger (name, email, phone, passport_no)
            VALUES (%s, %s, %s, %s)
        """

        values = (name, email, phone, passport_no)

        cursor.execute(query, values)
        connection.commit()

        print("Passenger added successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            raise Exception("Email or passport number already exists.")
        else:
            raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()

def get_total_passengers_count():
    connection = get_connection()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM Passenger")
        res = cursor.fetchone()
        return res['cnt'] if res else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_all_passengers():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Passenger"
        cursor.execute(query)

        passengers = cursor.fetchall()
        return passengers

    except Exception as e:
        print(f"Error fetching passengers: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def delete_passenger(passenger_id):
    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = "DELETE FROM Passenger WHERE passenger_id = %s"
        cursor.execute(query, (passenger_id,))

        if cursor.rowcount == 0:
            print("Passenger not found.")
            return False

        connection.commit()

        print("Passenger deleted successfully.")
        return True

    except Exception as e:
        connection.rollback()
        raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()
>>>>>>> Stashed changes

def update_passenger(passenger_id, name, email, phone, passport_no):
    """Update an existing passenger's details."""
    query = """
        UPDATE Passenger
        SET name = %s, email = %s, phone = %s, passport_no = %s
        WHERE passenger_id = %s
    """
    return execute_query(query, (name.strip(), email.strip(), phone.strip(), passport_no.strip(), passenger_id))

def delete_passenger(passenger_id):
    """Delete a passenger by ID."""
    query = "DELETE FROM Passenger WHERE passenger_id = %s"
    return execute_query(query, (passenger_id,))

<<<<<<< Updated upstream
def get_total_passengers_count():
    """Returns total count of passengers in the database."""
    query = "SELECT COUNT(*) as count FROM Passenger"
    res = fetch_one(query)
    return res['count'] if res else 0
=======
    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE Passenger
            SET name = %s,
                email = %s,
                phone = %s,
                passport_no = %s
            WHERE passenger_id = %s
        """

        values = (name, email, phone, passport_no, passenger_id)

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Passenger not found.")
            return False

        connection.commit()

        print("Passenger updated successfully.")
        return True


    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            raise Exception("Email or passport number already exists.")
        else:
            raise Exception(f"Database error: {str(e)}")

    finally:
        cursor.close()
        connection.close()
>>>>>>> Stashed changes
