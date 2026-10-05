CREATE DATABASE airline_reservation_db;

USE airline_reservation_db;
CREATE TABLE Passenger (
    passenger_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    passport_no VARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE Airport (
    airport_id INT PRIMARY KEY AUTO_INCREMENT,
    airport_code VARCHAR(10) NOT NULL UNIQUE,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);
CREATE TABLE Aircraft (
    aircraft_id INT PRIMARY KEY AUTO_INCREMENT,
    aircraft_model VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    CHECK (capacity > 0)
);

CREATE TABLE Flight (
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    flight_number VARCHAR(20) NOT NULL UNIQUE,
    aircraft_id INT NOT NULL,
    departure_airport_id INT NOT NULL,
    arrival_airport_id INT NOT NULL,
    departure_datetime DATETIME NOT NULL,
    arrival_datetime DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL,
    base_fare DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (aircraft_id)
        REFERENCES Aircraft(aircraft_id),

    FOREIGN KEY (departure_airport_id)
        REFERENCES Airport(airport_id),

    FOREIGN KEY (arrival_airport_id)
        REFERENCES Airport(airport_id),

    CHECK (base_fare >= 0),
    CHECK (arrival_datetime > departure_datetime)
);

CREATE TABLE Seat (
    seat_id INT PRIMARY KEY AUTO_INCREMENT,
    aircraft_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_class VARCHAR(20) NOT NULL,

    FOREIGN KEY (aircraft_id)
        REFERENCES Aircraft(aircraft_id),

    UNIQUE (aircraft_id, seat_number)
);
CREATE TABLE Reservation (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    passenger_id INT NOT NULL,
    flight_id INT NOT NULL,
    booking_date DATE NOT NULL,
    reservation_status VARCHAR(20) NOT NULL,

    FOREIGN KEY (passenger_id)
        REFERENCES Passenger(passenger_id),

    FOREIGN KEY (flight_id)
        REFERENCES Flight(flight_id)
);
CREATE TABLE Payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,

    FOREIGN KEY (reservation_id)
        REFERENCES Reservation(reservation_id),

    CHECK (amount >= 0)
);