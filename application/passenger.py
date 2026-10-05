from application.database import fetch_all, fetch_one, execute_query


# ============================================================
# GET ALL PASSENGERS
# ============================================================

def get_all_passengers():
    """Retrieve all passenger records from the database."""

    query = """
        SELECT
            passenger_id,
            name,
            email,
            phone,
            passport_no
        FROM Passenger
        ORDER BY passenger_id DESC
    """

    return fetch_all(query)


# ============================================================
# GET PASSENGER BY ID
# ============================================================

def get_passenger_by_id(passenger_id):
    """Retrieve a single passenger record by ID."""

    query = """
        SELECT
            passenger_id,
            name,
            email,
            phone,
            passport_no
        FROM Passenger
        WHERE passenger_id = %s
    """

    return fetch_one(query, (passenger_id,))


# ============================================================
# ADD PASSENGER
# ============================================================

def add_passenger(name, email, phone, passport_no):
    """Insert a new passenger record into the database."""

    # Basic validation
    if not name or not email or not phone or not passport_no:
        return False

    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    passport_no = passport_no.strip()

    if not name or not email or not phone or not passport_no:
        return False

    query = """
        INSERT INTO Passenger
            (name, email, phone, passport_no)
        VALUES
            (%s, %s, %s, %s)
    """

    return execute_query(
        query,
        (name, email, phone, passport_no)
    )


# ============================================================
# UPDATE PASSENGER
# ============================================================

def update_passenger(
    passenger_id,
    name,
    email,
    phone,
    passport_no
):
    """Update an existing passenger's details."""

    if not name or not email or not phone or not passport_no:
        return False

    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    passport_no = passport_no.strip()

    if not name or not email or not phone or not passport_no:
        return False

    query = """
        UPDATE Passenger
        SET
            name = %s,
            email = %s,
            phone = %s,
            passport_no = %s
        WHERE passenger_id = %s
    """

    return execute_query(
        query,
        (
            name,
            email,
            phone,
            passport_no,
            passenger_id
        )
    )


# ============================================================
# DELETE PASSENGER
# ============================================================

def delete_passenger(passenger_id):
    """Delete a passenger by ID."""

    query = """
        DELETE FROM Passenger
        WHERE passenger_id = %s
    """

    return execute_query(
        query,
        (passenger_id,)
    )


# ============================================================
# TOTAL PASSENGER COUNT
# ============================================================

def get_total_passengers_count():
    """Return the total number of passengers."""

    query = """
        SELECT COUNT(*) AS count
        FROM Passenger
    """

    result = fetch_one(query)

    if result:
        return result["count"]

    return 0