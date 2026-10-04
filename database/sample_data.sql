USE airline_reservation_db;
INSERT INTO Airport
(airport_code, airport_name, city, country)
VALUES
('HYD', 'Rajiv Gandhi International Airport', 'Hyderabad', 'India'),
('DEL', 'Indira Gandhi International Airport', 'Delhi', 'India'),
('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India'),
('BLR', 'Kempegowda International Airport', 'Bangalore', 'India'),
('MAA', 'Chennai International Airport', 'Chennai', 'India');

INSERT INTO Aircraft
(aircraft_model, capacity)
VALUES
('Airbus A320', 180),
('Boeing 737-800', 189),
('Airbus A321', 220),
('Boeing 787-9', 296),
('Airbus A350-900', 325);

INSERT INTO Passenger
(name, email, phone, passport_no)
VALUES
('Rahul Sharma', 'rahul.sharma@gmail.com', '9876543210', 'P1234567'),
('Priya Reddy', 'priya.reddy@gmail.com', '9876543211', 'P1234568'),
('Arjun Mehta', 'arjun.mehta@gmail.com', '9876543212', 'P1234569'),
('Ananya Singh', 'ananya.singh@gmail.com', '9876543213', 'P1234570'),
('Vikram Rao', 'vikram.rao@gmail.com', '9876543214', 'P1234571');

INSERT INTO Seat
(aircraft_id, seat_number, seat_class)
VALUES
(1, '1A', 'Business'),
(1, '1B', 'Business'),
(2, '10A', 'Economy'),
(2, '10B', 'Economy'),
(3, '15A', 'Economy');

INSERT INTO Flight
(flight_number, aircraft_id, departure_airport_id, arrival_airport_id,
 departure_datetime, arrival_datetime, status, base_fare)
VALUES
('AI101', 1, 1, 2, '2026-10-10 08:00:00', '2026-10-10 10:15:00', 'Scheduled', 5500.00),
('6E202', 2, 2, 3, '2026-10-11 11:30:00', '2026-10-11 13:45:00', 'Scheduled', 4800.00),
('UK303', 3, 3, 4, '2026-10-12 15:00:00', '2026-10-12 17:00:00', 'Scheduled', 5200.00),
('AI404', 4, 4, 5, '2026-10-13 18:30:00', '2026-10-13 20:45:00', 'Scheduled', 6200.00),
('6E505', 5, 5, 1, '2026-10-14 06:30:00', '2026-10-14 09:00:00', 'Scheduled', 5800.00);

INSERT INTO Reservation
(passenger_id, flight_id, booking_date, reservation_status)
VALUES
(1, 1, '2026-09-20', 'Confirmed'),
(2, 2, '2026-09-21', 'Confirmed'),
(3, 3, '2026-09-22', 'Confirmed'),
(4, 4, '2026-09-23', 'Pending'),
(5, 5, '2026-09-24', 'Confirmed');

INSERT INTO Payment
(reservation_id, amount, payment_method, payment_status, payment_date)
VALUES
(1, 5500.00, 'UPI', 'Paid', '2026-09-20'),
(2, 4800.00, 'Card', 'Paid', '2026-09-21'),
(3, 5200.00, 'UPI', 'Paid', '2026-09-22'),
(4, 6200.00, 'Card', 'Pending', '2026-09-23'),
(5, 5800.00, 'Net Banking', 'Paid', '2026-09-24');