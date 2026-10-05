from application.database import fetch_all, fetch_one, execute_query

def get_all_reservations():
    """Retrieve all reservations joined with passenger and flight info."""
    query = """
        SELECT 
            r.reservation_id,
            r.passenger_id,
            p.name AS passenger_name,
            p.email AS passenger_email,
            r.flight_id,
            f.flight_number,
            f.departure_datetime,
            f.arrival_datetime,
            r.booking_date,
            r.reservation_status
        FROM Reservation r
        JOIN Passenger p ON r.passenger_id = p.passenger_id
        JOIN Flight f ON r.flight_id = f.flight_id
        ORDER BY r.reservation_id DESC
    """
    return fetch_all(query)

def get_reservation_by_id(reservation_id):
    """Retrieve a single reservation by ID."""
    query = """
        SELECT 
            r.*,
            p.name AS passenger_name,
            f.flight_number
        FROM Reservation r
        JOIN Passenger p ON r.passenger_id = p.passenger_id
        JOIN Flight f ON r.flight_id = f.flight_id
        WHERE r.reservation_id = %s
    """
    return fetch_one(query, (reservation_id,))

def add_reservation(passenger_id, flight_id, booking_date, reservation_status):
    """Create a new reservation record."""
    query = """
        INSERT INTO Reservation (passenger_id, flight_id, booking_date, reservation_status)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (int(passenger_id), int(flight_id), str(booking_date), reservation_status.strip()))

<<<<<<< Updated upstream
def update_reservation_status(reservation_id, reservation_status):
    """Update status of a reservation."""
    query = """
        UPDATE Reservation
        SET reservation_status = %s
        WHERE reservation_id = %s
    """
    return execute_query(query, (reservation_status.strip(), int(reservation_id)))
=======
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

def get_total_reservations_count():
    connection = get_connection()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM Reservation")
        res = cursor.fetchone()
        return res['cnt'] if res else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_all_reservations():
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

def update_reservation_status(reservation_id, status):
    connection = get_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Reservation SET reservation_status = %s WHERE reservation_id = %s", (status, reservation_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
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
>>>>>>> Stashed changes

def delete_reservation(reservation_id):
    """Delete a reservation by ID."""
    query = "DELETE FROM Reservation WHERE reservation_id = %s"
    return execute_query(query, (int(reservation_id),))

def get_total_reservations_count():
    """Returns total reservation count."""
    query = "SELECT COUNT(*) as count FROM Reservation"
    res = fetch_one(query)
    return res['count'] if res else 0
