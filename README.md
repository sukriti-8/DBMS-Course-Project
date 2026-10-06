# Airline Reservation and Flight Operations Management System

## Project Overview
The Airline Reservation and Flight Operations Management System is a Database Management System project developed to manage airline-related information such as passengers, airports, aircraft, flights, reservations, seats, and payments.

The project uses MySQL as the database and Python with Streamlit to provide a simple user interface for viewing and managing the data.

## Objectives
- Manage passenger information.
- Manage airport and aircraft details.
- Manage flight information and schedules.
- Manage seat information.
- Manage flight reservations.
- Manage payment information.
- Perform SQL queries for retrieving and analysing data.
- Provide a user-friendly interface connected to the MySQL database.
- Demonstrate primary keys, foreign keys, constraints, relationships, and normalization.

## Scope
The system covers the basic database operations required for an airline reservation and flight operations system.

Users can:
- Add, view, update, and delete passenger records.
- View and manage flight information.
- Manage reservations.
- Manage payment details.
- View airport and aircraft information.
- Execute SQL queries for data retrieval and analysis.

## Technologies Used
- Python
- Streamlit
- MySQL
- mysql-connector-python
- Pandas
- Git
- GitHub
- MySQL Workbench
- draw.io

## Database Tables
1. Passenger – Stores passenger details such as name, email, phone number, and passport number.
2. Airport – Stores airport code, name, city, and country.
3. Aircraft – Stores aircraft model and capacity.
4. Flight – Stores flight number, aircraft, departure airport, arrival airport, schedule, status, and base fare.
5. Seat – Stores aircraft seat number and seat class.
6. Reservation – Stores passenger reservations for flights.
7. Payment – Stores payment details associated with reservations.

## Database Relationships
- One Passenger can have many Reservations.
- One Flight can have many Reservations.
- One Aircraft can operate many Flights.
- One Aircraft can have many Seats.
- One Airport can be the departure airport for many Flights.
- One Airport can be the arrival airport for many Flights.
- One Reservation has one Payment.

The database is designed and normalized up to Third Normal Form (3NF).

## System Architecture
User → Streamlit User Interface → Python Backend → MySQL Database

The Streamlit interface accepts user actions, the Python backend processes them, and the MySQL database stores and retrieves the information.

## Main Features

### Dashboard
The dashboard displays:
- Total passengers
- Total flights
- Total reservations
- Total payments
- Average flight base fare
- Payment method summary

### Passenger Management
- Add passengers
- View passengers
- Update passenger information
- Delete passengers

### Flight Management
- View flights
- Add flight details
- Update flight information
- Delete flights

### Reservation Management
- View reservations
- Add reservations
- Update reservation status
- Delete reservations

### Payment Management
- View payments
- Add payment details
- Delete payment records
- View payment summaries

## SQL Operations
The project demonstrates:
- SELECT
- WHERE
- ORDER BY
- JOIN
- GROUP BY
- HAVING
- COUNT()
- SUM()
- AVG()

Example:

SELECT * FROM Flight WHERE base_fare > 5000;

Example JOIN:

SELECT Passenger.name, Flight.flight_number
FROM Reservation
JOIN Passenger
ON Reservation.passenger_id = Passenger.passenger_id
JOIN Flight
ON Reservation.flight_id = Flight.flight_id;

## Project Structure
DBMS-Course-Project/
├── README.md
├── database/
│   ├── airline_database.sql
│   ├── sample_data.sql
│   ├── queries.sql
│   ├── ER_Diagram.png
│   └── ER_Diagram.drawio
├── application/
│   ├── app.py
│   ├── database.py
│   ├── passenger.py
│   ├── flight.py
│   ├── reservation.py
│   ├── payment.py
│   ├── airport.py
│   └── aircraft.py
├── tests/
├── Presentation/
└── Project-Report/

## How to Run the Project

### 1. Clone the Repository
git clone https://github.com/sukriti-8/DBMS-Course-Project.git

### 2. Open the Project
cd DBMS-Course-Project

### 3. Install Required Packages
pip install streamlit pandas mysql-connector-python

### 4. Set Up MySQL
Open MySQL Workbench and execute:

database/airline_database.sql

Then execute:

database/sample_data.sql

### 5. Run the Streamlit Application
python -m streamlit run application/app.py

## Sample Data
The database contains sample records for all major tables. Each major table contains at least 5 sample records for testing and demonstration.

## Testing
The system was tested for:
- Database table creation
- Primary and foreign key constraints
- Sample data insertion
- SQL query execution
- Passenger CRUD operations
- Flight CRUD operations
- Reservation operations
- Payment operations
- MySQL connectivity
- Streamlit UI functionality
- Changes made through the UI being reflected in the MySQL database

## Team Members

### Sukriti Gupta
Role: Database and SQL

Responsibilities:
- Database schema design
- SQL table creation
- Sample data
- SQL queries
- ER diagram
- Database normalization
- GitHub repository management

### Hrishika
Role: Python Backend and Database Connectivity

Responsibilities:
- Python backend
- MySQL connectivity
- CRUD operations
- Validation and error handling
- Project report

### Mithila
Role: Streamlit UI

Responsibilities:
- Streamlit user interface
- Dashboard
- Passenger, flight, reservation, and payment screens
- UI testing
- Project presentation

## Project Deliverables
- Database SQL files
- Sample data
- SQL queries
- ER diagram
- Python backend
- Streamlit UI
- Tests
- Project presentation
- Project report

## Conclusion
The project demonstrates how a relational database can be designed and implemented for an airline reservation and flight operations system.

It combines MySQL database management, SQL queries, Python backend development, and a Streamlit user interface to provide a functional system for managing airline-related data.

## Future Enhancements
- Online ticket booking and cancellation
- User authentication
- Real-time flight status
- Automatic seat availability tracking
- Email or SMS booking notifications
- Online payment gateway integration
- Advanced reporting and analytics

## GitHub Repository
https://github.com/sukriti-8/DBMS-Course-Project.git
