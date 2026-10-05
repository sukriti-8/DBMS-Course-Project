from application.database import get_connection


def add_reservation(passenger_id, flight_id, booking_date, reservation_status):
    if not passenger_id or not flight_id or not booking_date or not reservation_status:
        print("All reservation details are required.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO Reservation (
                passenger_id,
                flight_id,
                booking_date,
                reservation_status
            )
            VALUES (%s, %s, %s, %s)
        """

        values = (
            passenger_id,
            flight_id,
            booking_date,
            reservation_status
        )

        cursor.execute(query, values)
        connection.commit()

        print("Reservation added successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Cannot add or update a child row" in str(e):
            print("Passenger or flight does not exist.")
        else:
            print(f"Error adding reservation: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def get_reservations():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Reservation"
        cursor.execute(query)

        reservations = cursor.fetchall()
        return reservations

    except Exception as e:
        print(f"Error fetching reservations: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def update_reservation(
    reservation_id,
    passenger_id,
    flight_id,
    booking_date,
    reservation_status
):
    if not passenger_id or not flight_id or not booking_date or not reservation_status:
        print("All reservation details are required.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE Reservation
            SET passenger_id = %s,
                flight_id = %s,
                booking_date = %s,
                reservation_status = %s
            WHERE reservation_id = %s
        """

        values = (
            passenger_id,
            flight_id,
            booking_date,
            reservation_status,
            reservation_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Reservation not found.")
            return False

        connection.commit()

        print("Reservation updated successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Cannot add or update a child row" in str(e):
            print("Passenger or flight does not exist.")
        else:
            print(f"Error updating reservation: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def delete_reservation(reservation_id):
    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = "DELETE FROM Reservation WHERE reservation_id = %s"
        cursor.execute(query, (reservation_id,))

        if cursor.rowcount == 0:
            print("Reservation not found.")
            return False

        connection.commit()

        print("Reservation deleted successfully.")
        return True

    except Exception as e:
        connection.rollback()
        print(f"Error deleting reservation: {e}")
        return False

    finally:
        cursor.close()
        connection.close()