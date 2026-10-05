from application.database import get_connection


def add_payment(
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

def get_payments():
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

def delete_payment(payment_id):
    connection = get_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = "DELETE FROM Payment WHERE payment_id = %s"
        cursor.execute(query, (payment_id,))

        if cursor.rowcount == 0:
            print("Payment not found.")
            return False

        connection.commit()

        print("Payment deleted successfully.")
        return True

    except Exception as e:
        connection.rollback()
        print(f"Error deleting payment: {e}")
        return False

    finally:
        cursor.close()
        connection.close()