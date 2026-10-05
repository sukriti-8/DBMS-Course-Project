import datetime
import pandas as pd
import streamlit as st

# Import backend modules (Hrishika's Backend)
from application.database import get_db_connection, fetch_all, execute_query
import application.passenger as passenger_service
import application.flight as flight_service
import application.reservation as reservation_service
import application.payment as payment_service
import application.airport as airport_service
import application.aircraft as aircraft_service

# Page Configuration
st.set_page_config(
    page_title="SkyLine | Airline Reservation & Flight Operations System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Aesthetics
st.markdown("""
    <style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Container */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin-top: 6px;
        color: #93c5fd;
        font-size: 1.05rem;
    }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 8px;
    }

    /* Badge Tags */
    .badge-confirmed, .badge-paid {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-pending {
        background-color: #fef9c3;
        color: #a16207;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-scheduled {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Connection Banner */
    .db-status {
        font-size: 0.85rem;
        padding: 6px 12px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
        font-weight: 500;
    }
    .db-mysql {
        background-color: #0284c7;
        color: #ffffff;
    }
    .db-sqlite {
        background-color: #475569;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to inspect connection mode
_, db_engine = get_db_connection()

# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/isometric-line/100/airplane-take-off.png", width=70)
    st.title("SkyLine Management")
    st.caption("DBMS Course Project | Team Mithila, Sukriti, Hrishika")
    
    st.markdown("---")
    menu_choice = st.radio(
        "Navigation Menu",
        ["Dashboard", "Passengers", "Flights", "Reservations", "Payments", "SQL Verification Lab"],
        index=0
    )
    
    st.markdown("---")
    if db_engine == 'mysql':
        st.markdown('<div class="db-status db-mysql">⚡ Connected to Live MySQL DB</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="db-status db-sqlite">📦 Connected to Local SQLite Node</div>', unsafe_allow_html=True)
    
    st.caption("Architecture: Streamlit UI ➔ Python Backend ➔ MySQL")

# Header Render
st.markdown("""
    <div class="main-header">
        <h1>Airline Reservation & Flight Operations System</h1>
        <p>Comprehensive Database Management System for Passenger Bookings, Flight Schedules & Financial Transactions</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 1. DASHBOARD PAGE
# ==========================================
if menu_choice == "Dashboard":
    st.subheader("📊 Executive Overview & Live Metrics")
    
    # Fetch metrics from backend
    try:
        total_passengers = passenger_service.get_total_passengers_count()
        total_flights = flight_service.get_total_flights_count()
        total_reservations = reservation_service.get_total_reservations_count()
        total_payments = payment_service.get_total_payments_count()
        avg_fare = flight_service.get_average_base_fare()
    except Exception as e:
        st.error(f"Error connecting to backend services: {e}")
        total_passengers = total_flights = total_reservations = total_payments = 0
        avg_fare = 0.0

    # Layout 4 KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Passengers</div>
                <div class="metric-value">👤 {total_passengers}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Active Flights</div>
                <div class="metric-value">✈️ {total_flights}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Reservations</div>
                <div class="metric-value">🎫 {total_reservations}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Payments Processed</div>
                <div class="metric-value">💳 {total_payments}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    d_col1, d_col2 = st.columns([3, 2])
    with d_col1:
        st.write("### 🕒 Recent Flight Reservations")
        reservations = reservation_service.get_all_reservations()
        if reservations:
            df_res = pd.DataFrame(reservations)
            df_res_display = df_res[['reservation_id', 'passenger_name', 'flight_number', 'booking_date', 'reservation_status']]
            df_res_display.columns = ['ID', 'Passenger', 'Flight', 'Booking Date', 'Status']
            st.dataframe(df_res_display, use_container_width=True, hide_index=True)
        else:
            st.info("No reservations recorded yet.")

    with d_col2:
        st.write("### 💳 Payment Method Analytics")
        pay_summary = payment_service.get_payments_by_method_summary()
        if pay_summary:
            df_pay = pd.DataFrame(pay_summary)
            st.dataframe(df_pay.rename(columns={
                'payment_method': 'Method',
                'total_amount': 'Total (₹)',
                'transaction_count': 'Tx Count'
            }), use_container_width=True, hide_index=True)
            st.metric(label="Average Flight Base Fare", value=f"₹ {avg_fare:,.2f}")
        else:
            st.info("No payment analytics available.")

# ==========================================
# 2. PASSENGERS PAGE
# ==========================================
elif menu_choice == "Passengers":
    st.subheader("👤 Passenger Directory & Record Management")
    
    p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs(["📋 View All Passengers", "➕ Add Passenger", "✏️ Edit Passenger", "🗑️ Delete Passenger"])
    
    with p_tab1:
        passengers = passenger_service.get_all_passengers()
        if passengers:
            df_p = pd.DataFrame(passengers)
            df_p.columns = ['Passenger ID', 'Name', 'Email Address', 'Phone Number', 'Passport Number']
            st.dataframe(df_p, use_container_width=True, hide_index=True)
        else:
            st.info("No passengers found in database.")

    with p_tab2:
        st.write("#### Register New Passenger")
        with st.form("add_passenger_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
                email = st.text_input("Email Address *", placeholder="e.g. rahul@example.com")
            with col_b:
                phone = st.text_input("Phone Number *", placeholder="e.g. 9876543210")
                passport = st.text_input("Passport Number *", placeholder="e.g. P1234567")
            
            submit_btn = st.form_submit_button("Add Passenger")
            if submit_btn:
                if not name.strip():
                    st.error("Validation Error: Full Name is required.")
                elif not email.strip() or "@" not in email:
                    st.error("Validation Error: Valid Email Address is required.")
                elif not phone.strip():
                    st.error("Validation Error: Phone Number is required.")
                elif not passport.strip():
                    st.error("Validation Error: Passport Number is required.")
                else:
                    try:
                        passenger_service.add_passenger(name, email, phone, passport)
                        st.success(f"Successfully registered passenger: {name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to add passenger: {e}")

    with p_tab3:
        st.write("#### Update Passenger Details")
        passengers = passenger_service.get_all_passengers()
        if passengers:
            p_dict = {f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p for p in passengers}
            selected_p_str = st.selectbox("Select Passenger to Update", list(p_dict.keys()))
            selected_p = p_dict[selected_p_str]
            
            with st.form("update_passenger_form"):
                u_name = st.text_input("Full Name", value=selected_p['name'])
                u_email = st.text_input("Email Address", value=selected_p['email'])
                u_phone = st.text_input("Phone Number", value=selected_p['phone'])
                u_passport = st.text_input("Passport Number", value=selected_p['passport_no'])
                
                u_btn = st.form_submit_button("Update Details")
                if u_btn:
                    try:
                        passenger_service.update_passenger(selected_p['passenger_id'], u_name, u_email, u_phone, u_passport)
                        st.success("Passenger details updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating passenger: {e}")
        else:
            st.info("No passengers available to edit.")

    with p_tab4:
        st.write("#### Remove Passenger Record")
        passengers = passenger_service.get_all_passengers()
        if passengers:
            del_dict = {f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p['passenger_id'] for p in passengers}
            del_str = st.selectbox("Select Passenger to Delete", list(del_dict.keys()), key="del_p_select")
            
            if st.button("Delete Passenger", type="primary"):
                try:
                    passenger_service.delete_passenger(del_dict[del_str])
                    st.success("Passenger deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Cannot delete passenger (check foreign key constraints in reservations): {e}")
        else:
            st.info("No passengers available to delete.")

# ==========================================
# 3. FLIGHTS PAGE
# ==========================================
elif menu_choice == "Flights":
    st.subheader("✈️ Flight Schedules & Fleet Operations")
    
    f_tab1, f_tab2, f_tab3, f_tab4 = st.tabs(["📋 View All Flights", "➕ Schedule Flight", "✏️ Edit Flight", "🗑️ Cancel/Delete Flight"])
    
    airports = airport_service.get_all_airports()
    aircrafts = aircraft_service.get_all_aircrafts()
    
    airport_options = {f"{a['airport_code']} - {a['city']} ({a['airport_name']})": a['airport_id'] for a in airports} if airports else {}
    aircraft_options = {f"{ac['aircraft_model']} (Cap: {ac['capacity']})": ac['aircraft_id'] for ac in aircrafts} if aircrafts else {}

    with f_tab1:
        flights = flight_service.get_all_flights()
        if flights:
            df_f = pd.DataFrame(flights)
            df_f_display = df_f[[
                'flight_id', 'flight_number', 'aircraft_model', 'departure_code',
                'departure_city', 'arrival_code', 'arrival_city', 'departure_datetime',
                'arrival_datetime', 'status', 'base_fare'
            ]]
            df_f_display.columns = [
                'ID', 'Flight No', 'Aircraft', 'Dep Code', 'Dep City',
                'Arr Code', 'Arr City', 'Departure Time', 'Arrival Time', 'Status', 'Base Fare (₹)'
            ]
            st.dataframe(df_f_display, use_container_width=True, hide_index=True)
        else:
            st.info("No flights currently scheduled.")

    with f_tab2:
        st.write("#### Schedule New Flight")
        with st.form("add_flight_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                flight_num = st.text_input("Flight Number *", placeholder="e.g. AI102")
                aircraft_str = st.selectbox("Aircraft *", list(aircraft_options.keys()))
                dep_airport_str = st.selectbox("Departure Airport *", list(airport_options.keys()))
                arr_airport_str = st.selectbox("Arrival Airport *", list(airport_options.keys()), index=min(1, len(airport_options)-1))
            with f_col2:
                dep_dt = st.datetime_input("Departure Datetime *", datetime.datetime.now() + datetime.timedelta(days=1))
                arr_dt = st.datetime_input("Arrival Datetime *", datetime.datetime.now() + datetime.timedelta(days=1, hours=2))
                status = st.selectbox("Flight Status", ["Scheduled", "Delayed", "Departed", "Cancelled"])
                base_fare = st.number_input("Base Fare (₹) *", min_value=0.0, value=5000.0, step=100.0)

            f_submit = st.form_submit_button("Add Flight")
            if f_submit:
                dep_id = airport_options[dep_airport_str]
                arr_id = airport_options[arr_airport_str]
                
                if not flight_num.strip():
                    st.error("Validation Error: Flight Number is required.")
                elif dep_id == arr_id:
                    st.error("Validation Error: Departure airport cannot be the same as Arrival airport.")
                elif arr_dt <= dep_dt:
                    st.error("Validation Error: Arrival datetime must be strictly after Departure datetime.")
                elif base_fare < 0:
                    st.error("Validation Error: Base fare cannot be negative.")
                else:
                    try:
                        flight_service.add_flight(
                            flight_num, aircraft_options[aircraft_str], dep_id, arr_id,
                            dep_dt.strftime("%Y-%m-%d %H:%M:%S"), arr_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            status, base_fare
                        )
                        st.success(f"Flight {flight_num} scheduled successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to add flight: {e}")

    with f_tab3:
        st.write("#### Update Existing Flight")
        flights = flight_service.get_all_flights()
        if flights:
            f_dict = {f"{f['flight_id']} - {f['flight_number']} ({f['departure_code']} -> {f['arrival_code']})": f for f in flights}
            selected_f_str = st.selectbox("Select Flight to Update", list(f_dict.keys()))
            sel_f = f_dict[selected_f_str]
            
            with st.form("edit_flight_form"):
                uf_num = st.text_input("Flight Number", value=sel_f['flight_number'])
                uf_status = st.selectbox("Status", ["Scheduled", "Delayed", "Departed", "Cancelled"], index=["Scheduled", "Delayed", "Departed", "Cancelled"].index(sel_f['status']))
                uf_fare = st.number_input("Base Fare (₹)", min_value=0.0, value=float(sel_f['base_fare']))
                
                uf_btn = st.form_submit_button("Save Changes")
                if uf_btn:
                    try:
                        flight_service.update_flight(
                            sel_f['flight_id'], uf_num, sel_f['aircraft_id'],
                            sel_f['departure_airport_id'], sel_f['arrival_airport_id'],
                            sel_f['departure_datetime'], sel_f['arrival_datetime'],
                            uf_status, uf_fare
                        )
                        st.success("Flight updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating flight: {e}")
        else:
            st.info("No flights available to update.")

    with f_tab4:
        st.write("#### Delete Flight")
        flights = flight_service.get_all_flights()
        if flights:
            del_f_dict = {f"{f['flight_id']} - {f['flight_number']} ({f['departure_code']} -> {f['arrival_code']})": f['flight_id'] for f in flights}
            del_f_str = st.selectbox("Select Flight to Delete", list(del_f_dict.keys()), key="del_f_select")
            if st.button("Delete Flight", type="primary"):
                try:
                    flight_service.delete_flight(del_f_dict[del_f_str])
                    st.success("Flight record removed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Cannot delete flight (referenced in existing reservations): {e}")

# ==========================================
# 4. RESERVATIONS PAGE
# ==========================================
elif menu_choice == "Reservations":
    st.subheader("🎫 Reservation & Booking Management")
    
    r_tab1, r_tab2, r_tab3, r_tab4 = st.tabs(["📋 View Reservations", "➕ Create Reservation", "✏️ Update Status", "🗑️ Cancel Booking"])
    
    passengers = passenger_service.get_all_passengers()
    flights = flight_service.get_all_flights()
    
    pass_options = {f"{p['passenger_id']} - {p['name']} ({p['passport_no']})": p['passenger_id'] for p in passengers} if passengers else {}
    flight_options = {f"{f['flight_id']} - {f['flight_number']} ({f['departure_code']} ➔ {f['arrival_code']})": f['flight_id'] for f in flights} if flights else {}

    with r_tab1:
        reservations = reservation_service.get_all_reservations()
        if reservations:
            df_r = pd.DataFrame(reservations)
            df_r_display = df_r[['reservation_id', 'passenger_name', 'passenger_email', 'flight_number', 'departure_datetime', 'booking_date', 'reservation_status']]
            df_r_display.columns = ['Reservation ID', 'Passenger Name', 'Passenger Email', 'Flight No', 'Flight Dep Time', 'Booking Date', 'Status']
            st.dataframe(df_r_display, use_container_width=True, hide_index=True)
        else:
            st.info("No reservations recorded yet.")

    with r_tab2:
        st.write("#### New Passenger Booking")
        with st.form("create_reservation_form", clear_on_submit=True):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                selected_p = st.selectbox("Select Passenger *", list(pass_options.keys()))
                selected_f = st.selectbox("Select Flight *", list(flight_options.keys()))
            with r_col2:
                b_date = st.date_input("Booking Date", datetime.date.today())
                r_status = st.selectbox("Reservation Status", ["Confirmed", "Pending", "Cancelled"])

            r_submit = st.form_submit_button("Create Reservation")
            if r_submit:
                if not selected_p or not selected_f:
                    st.error("Please select both passenger and flight.")
                else:
                    try:
                        reservation_service.add_reservation(
                            pass_options[selected_p], flight_options[selected_f],
                            b_date.strftime("%Y-%m-%d"), r_status
                        )
                        st.success("Reservation created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create reservation: {e}")

    with r_tab3:
        st.write("#### Update Reservation Status")
        reservations = reservation_service.get_all_reservations()
        if reservations:
            res_dict = {f"Res #{r['reservation_id']} - {r['passenger_name']} ({r['flight_number']}) [{r['reservation_status']}]": r for r in reservations}
            selected_res_str = st.selectbox("Select Reservation", list(res_dict.keys()))
            sel_res = res_dict[selected_res_str]
            
            new_status = st.selectbox("New Reservation Status", ["Confirmed", "Pending", "Cancelled"], index=["Confirmed", "Pending", "Cancelled"].index(sel_res['reservation_status']))
            if st.button("Update Status"):
                try:
                    reservation_service.update_reservation_status(sel_res['reservation_id'], new_status)
                    st.success("Reservation status updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update status: {e}")

    with r_tab4:
        st.write("#### Cancel / Remove Reservation")
        reservations = reservation_service.get_all_reservations()
        if reservations:
            del_r_dict = {f"Res #{r['reservation_id']} - {r['passenger_name']} ({r['flight_number']})": r['reservation_id'] for r in reservations}
            del_r_str = st.selectbox("Select Reservation to Delete", list(del_r_dict.keys()), key="del_r_select")
            if st.button("Delete Reservation", type="primary"):
                try:
                    reservation_service.delete_reservation(del_r_dict[del_r_str])
                    st.success("Reservation cancelled and removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting reservation: {e}")

# ==========================================
# 5. PAYMENTS PAGE
# ==========================================
elif menu_choice == "Payments":
    st.subheader("💳 Financial Transactions & Payments")
    
    pay_tab1, pay_tab2, pay_tab3 = st.tabs(["📋 View All Payments", "➕ Record Payment", "🗑️ Delete Payment"])
    
    with pay_tab1:
        payments = payment_service.get_all_payments()
        if payments:
            df_pay = pd.DataFrame(payments)
            df_pay.columns = ['Payment ID', 'Res ID', 'Passenger', 'Flight', 'Amount (₹)', 'Payment Method', 'Status', 'Date']
            st.dataframe(df_pay, use_container_width=True, hide_index=True)
        else:
            st.info("No payment records found.")

    with pay_tab2:
        st.write("#### Process Reservation Payment")
        unpaid_res = payment_service.get_unpaid_reservations()
        if unpaid_res:
            unpaid_options = {f"Res #{r['reservation_id']} - {r['passenger_name']} ({r['flight_number']}) - Fare: ₹{r['base_fare']}": r for r in unpaid_res}
            sel_unpaid_str = st.selectbox("Select Reservation to Pay *", list(unpaid_options.keys()))
            sel_res_obj = unpaid_options[sel_unpaid_str]
            
            with st.form("add_payment_form", clear_on_submit=True):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    pay_amount = st.number_input("Payment Amount (₹) *", min_value=0.0, value=float(sel_res_obj['base_fare']))
                    pay_method = st.selectbox("Payment Method *", ["UPI", "Card", "Net Banking", "Cash"])
                with col_p2:
                    pay_status = st.selectbox("Payment Status *", ["Paid", "Pending", "Failed"])
                    pay_date = st.date_input("Payment Date", datetime.date.today())

                p_submit = st.form_submit_button("Record Payment")
                if p_submit:
                    if pay_amount < 0:
                        st.error("Validation Error: Amount cannot be negative.")
                    else:
                        try:
                            payment_service.add_payment(
                                sel_res_obj['reservation_id'], pay_amount, pay_method, pay_status, pay_date.strftime("%Y-%m-%d")
                            )
                            st.success(f"Payment of ₹{pay_amount} recorded successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to record payment: {e}")
        else:
            st.info("All existing reservations currently have payment records registered.")

    with pay_tab3:
        st.write("#### Remove Payment Record")
        payments = payment_service.get_all_payments()
        if payments:
            del_pay_dict = {f"Pay #{p['payment_id']} - Res #{p['reservation_id']} ({p['passenger_name']}) - ₹{p['amount']}": p['payment_id'] for p in payments}
            del_pay_str = st.selectbox("Select Payment to Remove", list(del_pay_dict.keys()), key="del_pay_select")
            if st.button("Delete Payment", type="primary"):
                try:
                    payment_service.delete_payment(del_pay_dict[del_pay_str])
                    st.success("Payment record deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting payment: {e}")

# ==========================================
# 6. SQL VERIFICATION LAB (PHASE 10 DEMO)
# ==========================================
elif menu_choice == "SQL Verification Lab":
    st.subheader("🔍 Live Database Verification Lab (DBMS Demonstration)")
    st.markdown("Execute pre-built SQL project queries or custom queries directly against the database to verify real-time data persistence.")
    
    preset_queries = {
        "Query 1: All Passengers": "SELECT * FROM Passenger;",
        "Query 2: Confirmed Reservations": "SELECT * FROM Reservation WHERE reservation_status = 'Confirmed';",
        "Query 3: Flights Ordered by Base Fare": "SELECT flight_number, base_fare FROM Flight ORDER BY base_fare DESC;",
        "Query 4: Flights with Airport Details": "SELECT f.flight_number, dep.airport_code AS dep_airport, arr.airport_code AS arr_airport, f.departure_datetime, f.arrival_datetime, f.base_fare FROM Flight f JOIN Airport dep ON f.departure_airport_id = dep.airport_id JOIN Airport arr ON f.arrival_airport_id = arr.airport_id;",
        "Query 5: Passengers and Reserved Flights": "SELECT p.name AS passenger_name, r.reservation_id, f.flight_number, r.booking_date, r.reservation_status FROM Passenger p JOIN Reservation r ON p.passenger_id = r.passenger_id JOIN Flight f ON r.flight_id = f.flight_id;",
        "Query 7: Total Payment Amount by Payment Method": "SELECT payment_method, SUM(amount) AS total_amount FROM Payment GROUP BY payment_method;",
        "Query 10: Complete Passenger Payment Details": "SELECT p.name AS passenger_name, r.reservation_id, f.flight_number, pay.amount, pay.payment_method, pay.payment_status FROM Passenger p JOIN Reservation r ON p.passenger_id = r.passenger_id JOIN Flight f ON r.flight_id = f.flight_id JOIN Payment pay ON r.reservation_id = pay.reservation_id;"
    }
    
    selected_query_name = st.selectbox("Choose Preset Project Query", list(preset_queries.keys()))
    sql_input = st.text_area("SQL Query Editor", value=preset_queries[selected_query_name], height=120)
    
    if st.button("Execute Query ▶️"):
        try:
            results = fetch_all(sql_input)
            if results:
                df_res = pd.DataFrame(results)
                st.write(f"### Query Output ({len(results)} rows)")
                st.dataframe(df_res, use_container_width=True)
            else:
                st.info("Query executed successfully. 0 rows returned or non-select query completed.")
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
