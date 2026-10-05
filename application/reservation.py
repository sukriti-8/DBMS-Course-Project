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

def update_reservation_status(reservation_id, reservation_status):
    """Update status of a reservation."""
    query = """
        UPDATE Reservation
        SET reservation_status = %s
        WHERE reservation_id = %s
    """
    return execute_query(query, (reservation_status.strip(), int(reservation_id)))

def delete_reservation(reservation_id):
    """Delete a reservation by ID."""
    query = "DELETE FROM Reservation WHERE reservation_id = %s"
    return execute_query(query, (int(reservation_id),))

def get_total_reservations_count():
    """Returns total reservation count."""
    query = "SELECT COUNT(*) as count FROM Reservation"
    res = fetch_one(query)
    return res['count'] if res else 0
