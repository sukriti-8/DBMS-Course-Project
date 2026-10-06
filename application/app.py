import os
import sys
import datetime

import pandas as pd
import streamlit as st

# Make the project root available to Python when running on Streamlit Cloud
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from application.database import get_db_connection, fetch_all
import application.passenger as passenger_service
import application.flight as flight_service
import application.reservation as reservation_service
import application.payment as payment_service
import application.airport as airport_service
import application.aircraft as aircraft_service


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkyLine | Airline Reservation System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,.20);
    }

    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
    }

    .main-header p {
        margin: 6px 0 0;
        color: #93c5fd;
        font-size: 1.05rem;
    }

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,.05);
    }

    .metric-title {
        font-size: .9rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 8px;
    }

    .db-status {
        font-size: .85rem;
        padding: 6px 12px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
        font-weight: 500;
    }

    .db-mysql {
        background: #0284c7;
        color: white;
    }

    .db-sqlite {
        background: #475569;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def run_service(function, *args, default=None, error_message=None):
    """Run a backend service safely and show a useful UI error."""
    try:
        return function(*args)
    except Exception as exc:
        if error_message:
            st.error(f"{error_message}: {exc}")
        else:
            st.error(str(exc))
        return default


def show_table(records, columns=None, rename=None, empty_message="No records found."):
    """Display a list of dictionaries as a Streamlit table."""
    if not records:
        st.info(empty_message)
        return

    df = pd.DataFrame(records)

    if columns:
        available = [c for c in columns if c in df.columns]
        if available:
            df = df[available]

    if rename:
        df = df.rename(columns=rename)

    st.dataframe(df, use_container_width=True, hide_index=True)


def metric_card(title, value, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{icon} {value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def refresh_success(message):
    st.success(message)
    st.rerun()


def make_passenger_options(passengers):
    return {
        f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p["passenger_id"]
        for p in passengers or []
    }


def make_flight_options(flights):
    return {
        f"{f['flight_id']} - {f['flight_number']} "
        f"({f['departure_code']} ➔ {f['arrival_code']})": f["flight_id"]
        for f in flights or []
    }


def get_database_status():
    """Return database engine plus the real connection error, if any."""
    try:
        result = get_db_connection()

        # Current project helper returns (connection, engine).
        if isinstance(result, tuple) and len(result) == 2:
            conn, engine = result
        else:
            # Backward-compatible with helpers that return only a connection.
            conn, engine = result, "mysql"

        if conn is None:
            return "unknown", "Database connection returned None."

        try:
            conn.close()
        except Exception:
            pass

        return str(engine).lower(), None

    except Exception as exc:
        return "unknown", str(exc)


DB_ENGINE, DB_ERROR = get_database_status()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image(
        "https://img.icons8.com/isometric-line/100/airplane-take-off.png",
        width=70,
    )

    st.title("SkyLine Management")
    st.caption("DBMS Course Project | Team Mithila, Sukriti, Hrishika")
    st.markdown("---")

    menu_choice = st.radio(
        "Navigation Menu",
        [
            "Dashboard",
            "Passengers",
            "Flights",
            "Reservations",
            "Payments",
            "SQL Verification Lab",
        ],
    )

    st.markdown("---")

    if DB_ENGINE == "mysql":
        st.markdown(
            '<div class="db-status db-mysql">⚡ Connected to Live MySQL DB</div>',
            unsafe_allow_html=True,
        )
    elif DB_ENGINE == "sqlite":
        st.markdown(
            '<div class="db-status db-sqlite">📦 Connected to Local SQLite DB</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Database connection unavailable.")
        if DB_ERROR:
            st.caption(f"Connection error: {DB_ERROR}")

    st.caption("Architecture: Streamlit UI ➜ Python Backend ➜ Database")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <h1>Airline Reservation & Flight Operations System</h1>
        <p>
            Comprehensive Database Management System for Passenger
            Bookings, Flight Schedules & Financial Transactions
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD
# ============================================================

if menu_choice == "Dashboard":
    st.subheader("📊 Executive Overview & Live Metrics")

    # Load the actual records once and derive the dashboard totals from them.
    # This avoids depending on separate COUNT helper functions that may be
    # inconsistent with the service functions used by the CRUD pages.
    dashboard_passengers = run_service(
        passenger_service.get_all_passengers,
        default=[],
        error_message="Unable to load passengers",
    )
    dashboard_flights = run_service(
        flight_service.get_all_flights,
        default=[],
        error_message="Unable to load flights",
    )
    dashboard_reservations = run_service(
        reservation_service.get_all_reservations,
        default=[],
        error_message="Unable to load reservations",
    )
    dashboard_payments = run_service(
        payment_service.get_all_payments,
        default=[],
        error_message="Unable to load payments",
    )

    total_passengers = len(dashboard_passengers or [])
    total_flights = len(dashboard_flights or [])
    total_reservations = len(dashboard_reservations or [])
    total_payments = len(dashboard_payments or [])

    fares = []
    for flight in dashboard_flights or []:
        try:
            fares.append(float(flight.get("base_fare", 0) or 0))
        except (TypeError, ValueError):
            pass
    avg_fare = sum(fares) / len(fares) if fares else 0.0

    cols = st.columns(4)
    cards = [
        ("Total Passengers", total_passengers, "👤"),
        ("Active Flights", total_flights, "✈️"),
        ("Reservations", total_reservations, "🎫"),
        ("Payments Processed", total_payments, "💳"),
    ]

    for col, (title, value, icon) in zip(cols, cards):
        with col:
            metric_card(title, value, icon)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        st.write("### 👥 Recent Passengers")
        passengers = dashboard_passengers
        show_table(
            passengers[:10] if passengers else [],
            columns=["passenger_id", "name", "email", "phone", "passport_no"],
            rename={
                "passenger_id": "ID",
                "name": "Passenger",
                "email": "Email",
                "phone": "Phone",
                "passport_no": "Passport",
            },
            empty_message="No passengers registered yet.",
        )

    with right:
        st.write("### 💳 Payment Method Analytics")
        pay_summary = run_service(
            payment_service.get_payments_by_method_summary,
            default=[],
            error_message="Unable to load payment analytics",
        )
        show_table(
            pay_summary,
            rename={
                "payment_method": "Method",
                "total_amount": "Total (₹)",
                "transaction_count": "Tx Count",
            },
            empty_message="No payment analytics available.",
        )
        st.metric("Average Flight Base Fare", f"₹ {avg_fare:,.2f}")

    st.markdown("---")
    st.write("### 🎫 Recent Flight Reservations")

    reservations = dashboard_reservations
    show_table(
        reservations[:10] if reservations else [],
        columns=[
            "reservation_id",
            "passenger_name",
            "flight_number",
            "booking_date",
            "reservation_status",
        ],
        rename={
            "reservation_id": "ID",
            "passenger_name": "Passenger",
            "flight_number": "Flight",
            "booking_date": "Booking Date",
            "reservation_status": "Status",
        },
        empty_message="No reservations recorded yet.",
    )


# ============================================================
# PASSENGERS
# ============================================================

elif menu_choice == "Passengers":
    st.subheader("👤 Passenger Directory & Record Management")

    tab_view, tab_add, tab_edit, tab_delete = st.tabs(
        ["📋 View All Passengers", "➕ Add Passenger", "✏️ Edit Passenger", "🗑️ Delete Passenger"]
    )

    with tab_view:
        passengers = run_service(
            passenger_service.get_all_passengers,
            default=[],
            error_message="Unable to load passengers",
        )
        show_table(
            passengers,
            columns=["passenger_id", "name", "email", "phone", "passport_no"],
            rename={
                "passenger_id": "Passenger ID",
                "name": "Name",
                "email": "Email Address",
                "phone": "Phone Number",
                "passport_no": "Passport Number",
            },
            empty_message="No passengers found in database.",
        )

    with tab_add:
        st.write("#### Register New Passenger")

        with st.form("add_passenger_form", clear_on_submit=True):
            c1, c2 = st.columns(2)

            with c1:
                name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
                email = st.text_input("Email Address *", placeholder="e.g. rahul@example.com")

            with c2:
                phone = st.text_input("Phone Number *", placeholder="e.g. 9876543210")
                passport = st.text_input("Passport Number *", placeholder="e.g. P1234567")

            submitted = st.form_submit_button("Add Passenger")

            if submitted:
                name = name.strip()
                email = email.strip()
                phone = phone.strip()
                passport = passport.strip()

                if not name:
                    st.error("Full Name is required.")
                elif "@" not in email:
                    st.error("Please enter a valid email address.")
                elif not phone:
                    st.error("Phone Number is required.")
                elif not passport:
                    st.error("Passport Number is required.")
                else:
                    result = run_service(
                        passenger_service.add_passenger,
                        name,
                        email,
                        phone,
                        passport,
                        default=False,
                        error_message="Failed to add passenger",
                    )
                    if result:
                        refresh_success(f"Successfully registered passenger: {name}")
                    else:
                        st.error("Passenger could not be added. Email or passport may already exist.")

    with tab_edit:
        st.write("#### Update Passenger Details")

        passengers = run_service(
            passenger_service.get_all_passengers,
            default=[],
            error_message="Unable to load passengers",
        )

        if not passengers:
            st.info("No passengers available to edit.")
        else:
            options = {
                f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p
                for p in passengers
            }

            selected = st.selectbox("Select Passenger to Update", list(options))
            passenger = options[selected]

            with st.form("update_passenger_form"):
                u_name = st.text_input("Full Name", value=passenger["name"])
                u_email = st.text_input("Email Address", value=passenger["email"])
                u_phone = st.text_input("Phone Number", value=passenger["phone"])
                u_passport = st.text_input("Passport Number", value=passenger["passport_no"])

                submitted = st.form_submit_button("Update Details")

                if submitted:
                    result = run_service(
                        passenger_service.update_passenger,
                        passenger["passenger_id"],
                        u_name.strip(),
                        u_email.strip(),
                        u_phone.strip(),
                        u_passport.strip(),
                        default=False,
                        error_message="Error updating passenger",
                    )
                    if result:
                        refresh_success("Passenger details updated successfully!")
                    else:
                        st.error("Passenger could not be updated.")

    with tab_delete:
        st.write("#### Remove Passenger Record")

        passengers = run_service(
            passenger_service.get_all_passengers,
            default=[],
            error_message="Unable to load passengers",
        )

        if not passengers:
            st.info("No passengers available to delete.")
        else:
            options = {
                f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p["passenger_id"]
                for p in passengers
            }

            selected = st.selectbox(
                "Select Passenger to Delete",
                list(options),
                key="delete_passenger_select",
            )

            if st.button("Delete Passenger", type="primary"):
                result = run_service(
                    passenger_service.delete_passenger,
                    options[selected],
                    default=False,
                    error_message="Cannot delete passenger",
                )
                if result:
                    refresh_success("Passenger deleted successfully!")
                else:
                    st.error(
                        "Passenger could not be deleted. "
                        "It may be referenced by a reservation."
                    )


# ============================================================
# FLIGHTS
# ============================================================

elif menu_choice == "Flights":
    st.subheader("✈️ Flight Schedules & Fleet Operations")

    tab_view, tab_add, tab_edit, tab_delete = st.tabs(
        ["📋 View All Flights", "➕ Schedule Flight", "✏️ Edit Flight", "🗑️ Delete Flight"]
    )

    airports = run_service(
        airport_service.get_all_airports,
        default=[],
        error_message="Unable to load airports",
    )
    aircrafts = run_service(
        aircraft_service.get_all_aircrafts,
        default=[],
        error_message="Unable to load aircraft",
    )

    airport_options = {
        f"{a['airport_code']} - {a['city']} ({a['airport_name']})": a["airport_id"]
        for a in airports or []
    }

    aircraft_options = {
        f"{a['aircraft_model']} (Cap: {a['capacity']})": a["aircraft_id"]
        for a in aircrafts or []
    }

    with tab_view:
        flights = run_service(
            flight_service.get_all_flights,
            default=[],
            error_message="Unable to load flights",
        )

        show_table(
            flights,
            columns=[
                "flight_id",
                "flight_number",
                "aircraft_model",
                "departure_code",
                "departure_city",
                "arrival_code",
                "arrival_city",
                "departure_datetime",
                "arrival_datetime",
                "status",
                "base_fare",
            ],
            rename={
                "flight_id": "ID",
                "flight_number": "Flight No",
                "aircraft_model": "Aircraft",
                "departure_code": "Dep Code",
                "departure_city": "Dep City",
                "arrival_code": "Arr Code",
                "arrival_city": "Arr City",
                "departure_datetime": "Departure Time",
                "arrival_datetime": "Arrival Time",
                "status": "Status",
                "base_fare": "Base Fare (₹)",
            },
            empty_message="No flights currently scheduled.",
        )

    with tab_add:
        st.write("#### Schedule New Flight")

        if not aircraft_options:
            st.warning("No aircraft records available.")
        elif len(airport_options) < 2:
            st.warning("At least two airports are required.")
        else:
            with st.form("add_flight_form", clear_on_submit=True):
                c1, c2 = st.columns(2)

                with c1:
                    flight_num = st.text_input("Flight Number *", placeholder="e.g. AI102")
                    aircraft_name = st.selectbox("Aircraft *", list(aircraft_options))
                    dep_airport = st.selectbox("Departure Airport *", list(airport_options))
                    arr_airport = st.selectbox(
                        "Arrival Airport *",
                        list(airport_options),
                        index=1,
                    )

                with c2:
                    now = datetime.datetime.now()
                    dep_dt = st.datetime_input(
                        "Departure Datetime *",
                        now + datetime.timedelta(days=1),
                    )
                    arr_dt = st.datetime_input(
                        "Arrival Datetime *",
                        now + datetime.timedelta(days=1, hours=2),
                    )
                    status = st.selectbox(
                        "Flight Status",
                        ["Scheduled", "Delayed", "Departed", "Cancelled"],
                    )
                    base_fare = st.number_input(
                        "Base Fare (₹) *",
                        min_value=0.0,
                        value=5000.0,
                        step=100.0,
                    )

                submitted = st.form_submit_button("Schedule Flight")

                if submitted:
                    if not flight_num.strip():
                        st.error("Flight Number is required.")
                    elif dep_airport == arr_airport:
                        st.error("Departure and arrival airports must be different.")
                    elif arr_dt <= dep_dt:
                        st.error("Arrival time must be after departure time.")
                    else:
                        result = run_service(
                            flight_service.add_flight,
                            flight_num.strip(),
                            aircraft_options[aircraft_name],
                            airport_options[dep_airport],
                            airport_options[arr_airport],
                            dep_dt,
                            arr_dt,
                            status,
                            base_fare,
                            default=False,
                            error_message="Failed to schedule flight",
                        )
                        if result:
                            refresh_success(f"Flight {flight_num} scheduled successfully!")
                        else:
                            st.error("Flight could not be added.")

    with tab_edit:
        st.write("#### Update Existing Flight")

        flights = run_service(
            flight_service.get_all_flights,
            default=[],
            error_message="Unable to load flights",
        )

        if not flights:
            st.info("No flights available to update.")
        else:
            options = {
                f"{f['flight_id']} - {f['flight_number']} "
                f"({f['departure_code']} -> {f['arrival_code']})": f
                for f in flights
            }

            selected = st.selectbox("Select Flight to Update", list(options))
            flight = options[selected]

            status_options = ["Scheduled", "Delayed", "Departed", "Cancelled"]
            current_status = flight.get("status", "Scheduled")
            if current_status not in status_options:
                current_status = "Scheduled"

            with st.form("edit_flight_form"):
                number = st.text_input("Flight Number", value=flight["flight_number"])
                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(current_status),
                )
                fare = st.number_input(
                    "Base Fare (₹)",
                    min_value=0.0,
                    value=float(flight["base_fare"]),
                )

                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    result = run_service(
                        flight_service.update_flight,
                        flight["flight_id"],
                        number.strip(),
                        flight["aircraft_id"],
                        flight["departure_airport_id"],
                        flight["arrival_airport_id"],
                        flight["departure_datetime"],
                        flight["arrival_datetime"],
                        new_status,
                        fare,
                        default=False,
                        error_message="Error updating flight",
                    )

                    if result:
                        refresh_success("Flight updated successfully!")
                    else:
                        st.error("Flight could not be updated.")

    with tab_delete:
        st.write("#### Delete Flight")

        flights = run_service(
            flight_service.get_all_flights,
            default=[],
            error_message="Unable to load flights",
        )

        if not flights:
            st.info("No flights available to delete.")
        else:
            options = {
                f"{f['flight_id']} - {f['flight_number']} "
                f"({f['departure_code']} -> {f['arrival_code']})": f["flight_id"]
                for f in flights
            }

            selected = st.selectbox(
                "Select Flight to Delete",
                list(options),
                key="delete_flight_select",
            )

            if st.button("Delete Flight", type="primary"):
                result = run_service(
                    flight_service.delete_flight,
                    options[selected],
                    default=False,
                    error_message="Cannot delete flight",
                )
                if result:
                    refresh_success("Flight record removed successfully!")
                else:
                    st.error(
                        "Flight could not be deleted. "
                        "It may be referenced by reservations."
                    )


# ============================================================
# RESERVATIONS
# ============================================================

elif menu_choice == "Reservations":
    st.subheader("🎫 Reservation & Booking Management")

    tab_view, tab_add, tab_edit, tab_delete = st.tabs(
        ["📋 View Reservations", "➕ Create Reservation", "✏️ Update Status", "🗑️ Cancel Booking"]
    )

    passengers = run_service(
        passenger_service.get_all_passengers,
        default=[],
        error_message="Unable to load passengers",
    )
    flights = run_service(
        flight_service.get_all_flights,
        default=[],
        error_message="Unable to load flights",
    )

    passenger_options = make_passenger_options(passengers)
    flight_options = make_flight_options(flights)

    with tab_view:
        reservations = run_service(
            reservation_service.get_all_reservations,
            default=[],
            error_message="Unable to load reservations",
        )

        show_table(
            reservations,
            columns=[
                "reservation_id",
                "passenger_name",
                "passenger_email",
                "flight_number",
                "departure_datetime",
                "booking_date",
                "reservation_status",
            ],
            rename={
                "reservation_id": "Reservation ID",
                "passenger_name": "Passenger Name",
                "passenger_email": "Passenger Email",
                "flight_number": "Flight No",
                "departure_datetime": "Flight Dep Time",
                "booking_date": "Booking Date",
                "reservation_status": "Status",
            },
            empty_message="No reservations recorded yet.",
        )

    with tab_add:
        st.write("#### New Passenger Booking")

        if not passenger_options:
            st.warning("No passengers available. Please add a passenger first.")
        elif not flight_options:
            st.warning("No flights available. Please schedule a flight first.")
        else:
            with st.form("create_reservation_form", clear_on_submit=True):
                c1, c2 = st.columns(2)

                with c1:
                    selected_passenger = st.selectbox(
                        "Select Passenger *",
                        list(passenger_options),
                    )
                    selected_flight = st.selectbox(
                        "Select Flight *",
                        list(flight_options),
                    )

                with c2:
                    booking_date = st.date_input(
                        "Booking Date",
                        datetime.date.today(),
                    )
                    reservation_status = st.selectbox(
                        "Reservation Status",
                        ["Confirmed", "Pending", "Cancelled"],
                    )

                submitted = st.form_submit_button("Create Reservation")

                if submitted:
                    result = run_service(
                        reservation_service.add_reservation,
                        passenger_options[selected_passenger],
                        flight_options[selected_flight],
                        booking_date.strftime("%Y-%m-%d"),
                        reservation_status,
                        default=False,
                        error_message="Failed to create reservation",
                    )

                    if result:
                        refresh_success("Reservation created successfully!")
                    else:
                        st.error("Reservation could not be created.")

    with tab_edit:
        st.write("#### Update Reservation Status")

        reservations = run_service(
            reservation_service.get_all_reservations,
            default=[],
            error_message="Unable to load reservations",
        )

        if not reservations:
            st.info("No reservations available.")
        else:
            options = {
                f"Res #{r['reservation_id']} - {r['passenger_name']} "
                f"({r['flight_number']}) [{r['reservation_status']}]": r
                for r in reservations
            }

            selected = st.selectbox("Select Reservation", list(options))
            reservation = options[selected]

            statuses = ["Confirmed", "Pending", "Cancelled"]
            current = reservation.get("reservation_status", "Pending")
            if current not in statuses:
                current = "Pending"

            new_status = st.selectbox(
                "New Reservation Status",
                statuses,
                index=statuses.index(current),
            )

            if st.button("Update Status"):
                result = run_service(
                    reservation_service.update_reservation_status,
                    reservation["reservation_id"],
                    new_status,
                    default=False,
                    error_message="Failed to update status",
                )
                if result:
                    refresh_success("Reservation status updated!")
                else:
                    st.error("Reservation could not be updated.")

    with tab_delete:
        st.write("#### Cancel / Remove Reservation")

        reservations = run_service(
            reservation_service.get_all_reservations,
            default=[],
            error_message="Unable to load reservations",
        )

        if not reservations:
            st.info("No reservations available.")
        else:
            options = {
                f"Res #{r['reservation_id']} - {r['passenger_name']} "
                f"({r['flight_number']})": r["reservation_id"]
                for r in reservations
            }

            selected = st.selectbox(
                "Select Reservation to Delete",
                list(options),
                key="delete_reservation_select",
            )

            if st.button("Delete Reservation", type="primary"):
                result = run_service(
                    reservation_service.delete_reservation,
                    options[selected],
                    default=False,
                    error_message="Error deleting reservation",
                )
                if result:
                    refresh_success("Reservation cancelled and removed!")
                else:
                    st.error("Reservation could not be deleted.")


# ============================================================
# PAYMENTS
# ============================================================

elif menu_choice == "Payments":
    st.subheader("💳 Financial Transactions & Payments")

    tab_view, tab_add, tab_delete = st.tabs(
        ["📋 View All Payments", "➕ Record Payment", "🗑️ Delete Payment"]
    )

    with tab_view:
        payments = run_service(
            payment_service.get_all_payments,
            default=[],
            error_message="Unable to load payments",
        )

        show_table(
            payments,
            rename={
                "payment_id": "Payment ID",
                "reservation_id": "Res ID",
                "passenger_name": "Passenger",
                "flight_number": "Flight",
                "amount": "Amount (₹)",
                "payment_method": "Payment Method",
                "payment_status": "Status",
                "payment_date": "Date",
            },
            empty_message="No payment records found.",
        )

    with tab_add:
        st.write("#### Process Reservation Payment")

        unpaid_reservations = run_service(
            payment_service.get_unpaid_reservations,
            default=[],
            error_message="Unable to load unpaid reservations",
        )

        if not unpaid_reservations:
            st.info("All existing reservations currently have payment records.")
        else:
            options = {
                f"Res #{r['reservation_id']} - {r['passenger_name']} "
                f"({r['flight_number']}) - Fare: ₹{r['base_fare']}": r
                for r in unpaid_reservations
            }

            selected = st.selectbox(
                "Select Reservation to Pay *",
                list(options),
            )
            reservation = options[selected]

            with st.form("add_payment_form", clear_on_submit=True):
                c1, c2 = st.columns(2)

                with c1:
                    amount = st.number_input(
                        "Payment Amount (₹) *",
                        min_value=0.0,
                        value=float(reservation["base_fare"]),
                        step=100.0,
                    )
                    method = st.selectbox(
                        "Payment Method *",
                        ["UPI", "Card", "Net Banking", "Cash"],
                    )

                with c2:
                    status = st.selectbox(
                        "Payment Status *",
                        ["Paid", "Pending", "Failed"],
                    )
                    payment_date = st.date_input(
                        "Payment Date",
                        datetime.date.today(),
                    )

                submitted = st.form_submit_button("Record Payment")

                if submitted:
                    result = run_service(
                        payment_service.add_payment,
                        reservation["reservation_id"],
                        amount,
                        method,
                        status,
                        payment_date.strftime("%Y-%m-%d"),
                        default=False,
                        error_message="Failed to record payment",
                    )

                    if result:
                        refresh_success(
                            f"Payment of ₹{amount:,.2f} recorded successfully!"
                        )
                    else:
                        st.error("Payment could not be recorded.")

    with tab_delete:
        st.write("#### Remove Payment Record")

        payments = run_service(
            payment_service.get_all_payments,
            default=[],
            error_message="Unable to load payments",
        )

        if not payments:
            st.info("No payment records available.")
        else:
            options = {
                f"Pay #{p['payment_id']} - Res #{p['reservation_id']} "
                f"({p['passenger_name']}) - ₹{p['amount']}": p["payment_id"]
                for p in payments
            }

            selected = st.selectbox(
                "Select Payment to Remove",
                list(options),
                key="delete_payment_select",
            )

            if st.button("Delete Payment", type="primary"):
                result = run_service(
                    payment_service.delete_payment,
                    options[selected],
                    default=False,
                    error_message="Error deleting payment",
                )

                if result:
                    refresh_success("Payment record deleted!")
                else:
                    st.error("Payment could not be deleted.")


# ============================================================
# SQL VERIFICATION LAB
# ============================================================

elif menu_choice == "SQL Verification Lab":
    st.subheader("🔍 Live Database Verification Lab")
    st.caption("Execute project SQL queries against the connected database.")

    preset_queries = {
        "Query 1: All Passengers":
            "SELECT * FROM Passenger;",

        "Query 2: Confirmed Reservations":
            """
            SELECT *
            FROM Reservation
            WHERE reservation_status = 'Confirmed';
            """,

        "Query 3: Flights Ordered by Base Fare":
            """
            SELECT flight_number, base_fare
            FROM Flight
            ORDER BY base_fare DESC;
            """,

        "Query 4: Flights with Airport Details":
            """
            SELECT
                f.flight_number,
                dep.airport_code AS dep_airport,
                arr.airport_code AS arr_airport,
                f.departure_datetime,
                f.arrival_datetime,
                f.base_fare
            FROM Flight f
            JOIN Airport dep
                ON f.departure_airport_id = dep.airport_id
            JOIN Airport arr
                ON f.arrival_airport_id = arr.airport_id;
            """,

        "Query 5: Passengers and Reserved Flights":
            """
            SELECT
                p.name AS passenger_name,
                r.reservation_id,
                f.flight_number,
                r.booking_date,
                r.reservation_status
            FROM Passenger p
            JOIN Reservation r
                ON p.passenger_id = r.passenger_id
            JOIN Flight f
                ON r.flight_id = f.flight_id;
            """,

        "Query 7: Total Payment Amount by Payment Method":
            """
            SELECT
                payment_method,
                SUM(amount) AS total_amount
            FROM Payment
            GROUP BY payment_method;
            """,

        "Query 10: Complete Passenger Payment Details":
            """
            SELECT
                p.name AS passenger_name,
                r.reservation_id,
                f.flight_number,
                pay.amount,
                pay.payment_method,
                pay.payment_status
            FROM Passenger p
            JOIN Reservation r
                ON p.passenger_id = r.passenger_id
            JOIN Flight f
                ON r.flight_id = f.flight_id
            JOIN Payment pay
                ON r.reservation_id = pay.reservation_id;
            """,
    }

    selected_query = st.selectbox(
        "Choose Preset Project Query",
        list(preset_queries),
    )

    sql = st.text_area(
        "SQL Query Editor",
        value=preset_queries[selected_query],
        height=220,
    )

    if st.button("Execute Query ▶️", type="primary"):
        sql = sql.strip()

        if not sql:
            st.warning("Please enter an SQL query.")
        else:
            try:
                results = fetch_all(sql)

                if results:
                    st.write(f"### Query Output ({len(results)} rows)")
                    st.dataframe(
                        pd.DataFrame(results),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.success("Query executed successfully. 0 rows returned.")

            except Exception as exc:
                st.error(f"SQL Execution Error: {exc}")
