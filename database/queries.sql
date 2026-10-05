USE airline_reservation_db;
-- Query 1: Display all passengers
SELECT *
FROM Passenger;
-- Query 2: Display confirmed reservations
SELECT *
FROM Reservation
WHERE reservation_status = 'Confirmed';
-- Query 3: Display flights ordered by base fare
SELECT flight_number, base_fare
FROM Flight
ORDER BY base_fare DESC;
-- Query 4: Display flights with departure and arrival airports
SELECT
    f.flight_number,
    dep.airport_code AS departure_airport,
    arr.airport_code AS arrival_airport,
    f.departure_datetime,
    f.arrival_datetime,
    f.base_fare
FROM Flight f
JOIN Airport dep
    ON f.departure_airport_id = dep.airport_id
JOIN Airport arr
    ON f.arrival_airport_id = arr.airport_id;

-- Query 5: Display passengers and their reserved flights
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

-- Query 6: Count reservations for each flight
SELECT
    f.flight_number,
    COUNT(r.reservation_id) AS total_reservations
FROM Flight f
LEFT JOIN Reservation r
    ON f.flight_id = r.flight_id
GROUP BY f.flight_id, f.flight_number;

-- Query 7: Calculate total payment amount by payment method
SELECT
    payment_method,
    SUM(amount) AS total_amount
FROM Payment
GROUP BY payment_method;

-- Query 8: Calculate the average base fare of flights
SELECT
    AVG(base_fare) AS average_fare
FROM Flight;

-- Query 9: Show payment methods with total amount greater than 5000
SELECT
    payment_method,
    SUM(amount) AS total_amount
FROM Payment
GROUP BY payment_method
HAVING SUM(amount) > 5000;

-- Query 10: Display passenger payment details
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

-- Query 11: Display flights with base fare above 5000
SELECT
    flight_number,
    base_fare,
    status
FROM Flight
WHERE base_fare > 5000
ORDER BY base_fare DESC;