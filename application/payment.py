from application.database import fetch_all, fetch_one, execute_query

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
        JOIN Reservation r ON pay.reservation_id = r.reservation_id
        JOIN Passenger p ON r.passenger_id = p.passenger_id
        JOIN Flight f ON r.flight_id = f.flight_id
        ORDER BY pay.payment_id DESC
    """
    return fetch_all(query)

def get_payment_by_id(payment_id):
    """Retrieve payment by ID."""
    query = "SELECT * FROM Payment WHERE payment_id = %s"
    return fetch_one(query, (payment_id,))

def get_unpaid_reservations():
    """Returns reservations that do not yet have a payment record (Enforces 1:1 constraint)."""
    query = """
        SELECT 
            r.reservation_id,
            p.name AS passenger_name,
            f.flight_number,
            f.base_fare
        FROM Reservation r
        JOIN Passenger p ON r.passenger_id = p.passenger_id
        JOIN Flight f ON r.flight_id = f.flight_id
        LEFT JOIN Payment pay ON r.reservation_id = pay.reservation_id
        WHERE pay.payment_id IS NULL
        ORDER BY r.reservation_id DESC
    """
    return fetch_all(query)

<<<<<<< Updated upstream
def add_payment(reservation_id, amount, payment_method, payment_status, payment_date):
    """Insert a new payment record for a reservation."""
    query = """
        INSERT INTO Payment (reservation_id, amount, payment_method, payment_status, payment_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        int(reservation_id),
        float(amount),
        payment_method.strip(),
        payment_status.strip(),
        str(payment_date)
    ))
=======
    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

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

        values = (
            reservation_id,
            amount,
            payment_method,
            payment_status,
            payment_date
        )

        cursor.execute(query, values)
        connection.commit()

        print("Payment added successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            print("Payment already exists for this reservation.")
        elif "Cannot add or update a child row" in str(e):
            print("Reservation does not exist.")
        else:
            print(f"Error adding payment: {e}")

        return False

    finally:
        cursor.close()
        connection.close()

def get_total_payments_count():
    connection = get_connection()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM Payment")
        res = cursor.fetchone()
        return res['cnt'] if res else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_payments_by_method_summary():
    connection = get_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT payment_method, COUNT(*) as cnt, SUM(amount) as total FROM Payment GROUP BY payment_method")
        res = cursor.fetchall()
        # app.py expects something? Let's return the rows
        # Actually app.py probably uses it for a chart.
        return res
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_unpaid_reservations():
    connection = get_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservation WHERE reservation_status != 'Paid'")
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_all_payments():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Payment"
        cursor.execute(query)

        payments = cursor.fetchall()
        return payments

    except Exception as e:
        print(f"Error fetching payments: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def update_payment(
    payment_id,
    reservation_id,
    amount,
    payment_method,
    payment_status,
    payment_date
):
    if not reservation_id or amount is None or not payment_method or not payment_status or not payment_date:
        print("All payment details are required.")
        return False

    if amount < 0:
        print("Payment amount cannot be negative.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            UPDATE Payment
            SET reservation_id = %s,
                amount = %s,
                payment_method = %s,
                payment_status = %s,
                payment_date = %s
            WHERE payment_id = %s
        """

        values = (
            reservation_id,
            amount,
            payment_method,
            payment_status,
            payment_date,
            payment_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Payment not found.")
            return False

        connection.commit()

        print("Payment updated successfully.")
        return True

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            print("Payment already exists for this reservation.")
        elif "Cannot add or update a child row" in str(e):
            print("Reservation does not exist.")
        else:
            print(f"Error updating payment: {e}")

        return False

    finally:
        cursor.close()
        connection.close()
>>>>>>> Stashed changes

def delete_payment(payment_id):
    """Delete a payment by ID."""
    query = "DELETE FROM Payment WHERE payment_id = %s"
    return execute_query(query, (int(payment_id),))

def get_total_payments_count():
    """Returns total payment count."""
    query = "SELECT COUNT(*) as count FROM Payment"
    res = fetch_one(query)
    return res['count'] if res else 0

def get_payments_by_method_summary():
    """Group by payment method and return total amounts (Query 7)."""
    query = """
        SELECT payment_method, SUM(amount) AS total_amount, COUNT(*) as transaction_count
        FROM Payment
        GROUP BY payment_method
    """
    return fetch_all(query)
