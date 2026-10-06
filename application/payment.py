from application.database import fetch_all, fetch_one, execute_query


# ============================================================
# GET ALL PAYMENTS
# ============================================================

def get_all_payments():
    """Retrieve all payment records with associated passenger and reservation details."""

    query = """
        SELECT
            pay.payment_id,
            pay.reservation_id,
            p.name AS passenger_name,
            f.flight_number,
            pay.amount,
            pay.payment_method,
            pay.payment_status,
            pay.payment_date
        FROM Payment pay
        JOIN Reservation r
            ON pay.reservation_id = r.reservation_id
        JOIN Passenger p
            ON r.passenger_id = p.passenger_id
        JOIN Flight f
            ON r.flight_id = f.flight_id
        ORDER BY pay.payment_id DESC
    """

    return fetch_all(query)


# ============================================================
# GET PAYMENT BY ID
# ============================================================

def get_payment_by_id(payment_id):
    """Retrieve payment by ID."""

    query = """
        SELECT *
        FROM Payment
        WHERE payment_id = %s
    """

    return fetch_one(query, (payment_id,))


# ============================================================
# GET UNPAID RESERVATIONS
# ============================================================

def get_unpaid_reservations():
    """Return reservations that do not yet have a payment record."""

    query = """
        SELECT
            r.reservation_id,
            p.name AS passenger_name,
            f.flight_number,
            f.base_fare
        FROM Reservation r
        JOIN Passenger p
            ON r.passenger_id = p.passenger_id
        JOIN Flight f
            ON r.flight_id = f.flight_id
        LEFT JOIN Payment pay
            ON r.reservation_id = pay.reservation_id
        WHERE pay.payment_id IS NULL
        ORDER BY r.reservation_id DESC
    """

    return fetch_all(query)


# ============================================================
# ADD PAYMENT
# ============================================================

def add_payment(
    reservation_id,
    amount,
    payment_method,
    payment_status,
    payment_date
):
    """Insert a new payment record for a reservation."""

    if (
        not reservation_id
        or amount is None
        or not payment_method
        or not payment_status
        or not payment_date
    ):
        print("All payment details are required.")
        return False

    if float(amount) < 0:
        print("Payment amount cannot be negative.")
        return False

    query = """
        INSERT INTO Payment (
            reservation_id,
            amount,
            payment_method,
            payment_status,
            payment_date
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        return execute_query(
            query,
            (
                int(reservation_id),
                float(amount),
                payment_method.strip(),
                payment_status.strip(),
                str(payment_date)
            )
        )

    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Payment already exists for this reservation.")
        elif "Cannot add or update a child row" in str(e):
            print("Reservation does not exist.")
        else:
            print(f"Error adding payment: {e}")

        return False


# ============================================================
# GET PAYMENTS
# ============================================================

def get_payments():
    """Retrieve all payment records."""

    query = """
        SELECT *
        FROM Payment
        ORDER BY payment_id DESC
    """

    return fetch_all(query)


# ============================================================
# UPDATE PAYMENT
# ============================================================

def update_payment(
    payment_id,
    reservation_id,
    amount,
    payment_method,
    payment_status,
    payment_date
):
    """Update an existing payment record."""

    if (
        not reservation_id
        or amount is None
        or not payment_method
        or not payment_status
        or not payment_date
    ):
        print("All payment details are required.")
        return False

    if float(amount) < 0:
        print("Payment amount cannot be negative.")
        return False

    query = """
        UPDATE Payment
        SET
            reservation_id = %s,
            amount = %s,
            payment_method = %s,
            payment_status = %s,
            payment_date = %s
        WHERE payment_id = %s
    """

    try:
        return execute_query(
            query,
            (
                int(reservation_id),
                float(amount),
                payment_method.strip(),
                payment_status.strip(),
                str(payment_date),
                int(payment_id)
            )
        )

    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Payment already exists for this reservation.")
        elif "Cannot add or update a child row" in str(e):
            print("Reservation does not exist.")
        else:
            print(f"Error updating payment: {e}")

        return False


# ============================================================
# DELETE PAYMENT
# ============================================================

def delete_payment(payment_id):
    """Delete a payment by ID."""

    query = """
        DELETE FROM Payment
        WHERE payment_id = %s
    """

    try:
        return execute_query(
            query,
            (int(payment_id),)
        )

    except Exception as e:
        print(f"Error deleting payment: {e}")
        return False


# ============================================================
# TOTAL PAYMENT COUNT
# ============================================================

def get_total_payments_count():
    """Returns total payment count."""

    query = """
        SELECT COUNT(*) AS count
        FROM Payment
    """

    result = fetch_one(query)

    return result["count"] if result else 0


# ============================================================
# PAYMENT METHOD SUMMARY
# ============================================================

def get_payments_by_method_summary():
    """Group payments by payment method and return total amounts."""

    query = """
        SELECT
            payment_method,
            SUM(amount) AS total_amount,
            COUNT(*) AS transaction_count
        FROM Payment
        GROUP BY payment_method
    """

    return fetch_all(query)