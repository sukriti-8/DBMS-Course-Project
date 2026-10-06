from application.database import fetch_all, fetch_one, execute_query


# ============================================================
# GET ALL RESERVATIONS
# ============================================================

def get_all_reservations():
    """Retrieve all reservations joined with passenger and flight information."""

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
        JOIN Passenger p
            ON r.passenger_id = p.passenger_id
        JOIN Flight f
            ON r.flight_id = f.flight_id
        ORDER BY r.reservation_id DESC
    """

    return fetch_all(query)


# ============================================================
# GET RESERVATION BY ID
# ============================================================

def get_reservation_by_id(reservation_id):
    """Retrieve a single reservation by ID."""

    query = """
        SELECT
            r.*,
            p.name AS passenger_name,
            f.flight_number
        FROM Reservation r
        JOIN Passenger p
            ON r.passenger_id = p.passenger_id
        JOIN Flight f
            ON r.flight_id = f.flight_id
        WHERE r.reservation_id = %s
    """

    return fetch_one(query, (reservation_id,))


# ============================================================
# ADD RESERVATION
# ============================================================

def add_reservation(
    passenger_id,
    flight_id,
    booking_date,
    reservation_status
):
    """Create a new reservation record."""

    if not passenger_id or not flight_id or not booking_date or not reservation_status:
        print("All reservation details are required.")
        return False

    query = """
        INSERT INTO Reservation (
            passenger_id,
            flight_id,
            booking_date,
            reservation_status
        )
        VALUES (%s, %s, %s, %s)
    """

    try:
        return execute_query(
            query,
            (
                int(passenger_id),
                int(flight_id),
                str(booking_date),
                reservation_status.strip()
            )
        )

    except Exception as e:
        if "Cannot add or update a child row" in str(e):
            print("Passenger or flight does not exist.")
        else:
            print(f"Error adding reservation: {e}")

        return False


# ============================================================
# GET RESERVATIONS
# ============================================================

def get_reservations():
    """Retrieve all reservations."""

    query = """
        SELECT *
        FROM Reservation
        ORDER BY reservation_id DESC
    """

    return fetch_all(query)


# ============================================================
# UPDATE RESERVATION
# ============================================================

def update_reservation(
    reservation_id,
    passenger_id,
    flight_id,
    booking_date,
    reservation_status
):
    """Update an existing reservation."""

    if not passenger_id or not flight_id or not booking_date or not reservation_status:
        print("All reservation details are required.")
        return False

    query = """
        UPDATE Reservation
        SET
            passenger_id = %s,
            flight_id = %s,
            booking_date = %s,
            reservation_status = %s
        WHERE reservation_id = %s
    """

    try:
        return execute_query(
            query,
            (
                int(passenger_id),
                int(flight_id),
                str(booking_date),
                reservation_status.strip(),
                int(reservation_id)
            )
        )

    except Exception as e:
        if "Cannot add or update a child row" in str(e):
            print("Passenger or flight does not exist.")
        else:
            print(f"Error updating reservation: {e}")

        return False


# ============================================================
# UPDATE RESERVATION STATUS
# ============================================================

def update_reservation_status(
    reservation_id,
    reservation_status
):
    """Update only the status of a reservation."""

    if not reservation_status:
        print("Reservation status is required.")
        return False

    query = """
        UPDATE Reservation
        SET reservation_status = %s
        WHERE reservation_id = %s
    """

    try:
        return execute_query(
            query,
            (
                reservation_status.strip(),
                int(reservation_id)
            )
        )

    except Exception as e:
        print(f"Error updating reservation status: {e}")
        return False


# ============================================================
# DELETE RESERVATION
# ============================================================

def delete_reservation(reservation_id):
    """Delete a reservation by ID."""

    query = """
        DELETE FROM Reservation
        WHERE reservation_id = %s
    """

    try:
        return execute_query(
            query,
            (int(reservation_id),)
        )

    except Exception as e:
        print(f"Error deleting reservation: {e}")
        return False


# ============================================================
# TOTAL RESERVATION COUNT
# ============================================================

def get_total_reservations_count():
    """Returns total reservation count."""

    query = """
        SELECT COUNT(*) AS count
        FROM Reservation
    """

    result = fetch_one(query)

    return result["count"] if result else 0