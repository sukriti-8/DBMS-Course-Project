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

    if not name or not email or not phone or not passport_no:
        print("All passenger details are required.")
        return False

    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    passport_no = passport_no.strip()

    if not name or not email or not phone or not passport_no:
        print("All passenger details are required.")
        return False

    query = """
        INSERT INTO Passenger
            (name, email, phone, passport_no)
        VALUES
            (%s, %s, %s, %s)
    """

    try:
        return execute_query(
            query,
            (name, email, phone, passport_no)
        )

    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Email or passport number already exists.")
        else:
            print(f"Error adding passenger: {e}")

        return False


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
        print("All passenger details are required.")
        return False

    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    passport_no = passport_no.strip()

    if not name or not email or not phone or not passport_no:
        print("All passenger details are required.")
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

    try:
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

    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Email or passport number already exists.")
        else:
            print(f"Error updating passenger: {e}")

        return False


# ============================================================
# DELETE PASSENGER
# ============================================================

def delete_passenger(passenger_id):
    """Delete a passenger by ID."""

    query = """
        DELETE FROM Passenger
        WHERE passenger_id = %s
    """

    try:
        return execute_query(
            query,
            (passenger_id,)
        )

    except Exception as e:
        print(f"Error deleting passenger: {e}")
        return False


# ============================================================
# GET PASSENGERS
# ============================================================

def get_passengers():
    """Retrieve all passengers."""

    query = """
        SELECT *
        FROM Passenger
        ORDER BY passenger_id DESC
    """

    return fetch_all(query)


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