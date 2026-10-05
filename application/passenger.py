from application.database import get_connection
def add_passenger(name, email, phone, passport_no):
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
            print("Email or passport number already exists.")
        else:
            print(f"Error adding passenger: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def get_passengers():
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
        print(f"Error deleting passenger: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def update_passenger(passenger_id, name, email, phone, passport_no):
    if not name or not email or not phone or not passport_no:
        print("All passenger details are required.")
        return False

    connection = get_connection()

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
            print("Email or passport number already exists.")
        else:
            print(f"Error updating passenger: {e}")

        return False

    finally:
        cursor.close()
        connection.close()