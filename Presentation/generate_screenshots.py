import os
import matplotlib.pyplot as plt

def create_screenshot_assets():
    target_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(target_dir, exist_ok=True)
    
    screenshots = [
        ("1_dashboard.png", "SkyLine DBMS - Executive Dashboard", "Total Passengers: 25 | Active Flights: 12 | Reservations: 18 | Payments: 15\nLive DB Engine: MySQL (airline_reservation_db)"),
        ("2_passenger_page.png", "Passenger Directory & Records", "Passenger Table: ID, Name, Email, Phone, Passport Number\n5 Active Records Loaded from MySQL"),
        ("3_passenger_insertion_form.png", "New Passenger Registration Form", "Fields: Name='Rahul Sharma', Email='rahul.sharma@gmail.com'\nPhone='9876543210', Passport='P1234567'\nAction: [ Add Passenger ]"),
        ("4_passenger_after_insertion.png", "Database After Insertion", "Success Message: 'Passenger registered successfully!'\nMySQL Table SELECT * FROM Passenger; -> New Record Added"),
        ("5_passenger_deletion.png", "Passenger Deletion Confirmation", "Select Passenger: ID #6 - Rahul Sharma\nAction: [ Delete Passenger ] -> MySQL DELETE executed"),
        ("6_flight_page.png", "Flight Management UI", "Flights: AI101 (HYD -> DEL), 6E202 (DEL -> BOM)\nForeign-key Friendly Dropdowns for Aircraft & Airports"),
        ("7_reservation_page.png", "Reservation Booking UI", "Fields: Passenger Dropdown + Flight Dropdown + Booking Date\nStatus: Confirmed / Pending"),
        ("8_payment_page.png", "Payment Processing UI", "Reservation #1 -> Amount: ₹5500.00 | Method: UPI | Status: Paid\nConstraint Enforcement: 1-to-1 Unique Reservation Payment"),
        ("db_select_before.png", "MySQL Workbench: SELECT * FROM Passenger (Before)", "+--------------+--------------+-----------------------+------------+-------------+\n| passenger_id | name         | email                 | phone      | passport_no |\n+--------------+--------------+-----------------------+------------+-------------+\n| 1            | Rahul Sharma | rahul.sharma@gmail.com| 9876543210 | P1234567    |\n+--------------+--------------+-----------------------+------------+-------------+"),
        ("db_select_after.png", "MySQL Workbench: SELECT * FROM Passenger (After Insert/Delete)", "+--------------+--------------+-----------------------+------------+-------------+\n| passenger_id | name         | email                 | phone      | passport_no |\n+--------------+--------------+-----------------------+------------+-------------+\n| 1            | Rahul Sharma | rahul.sharma@gmail.com| 9876543210 | P1234567    |\n| 6            | New User     | new.user@gmail.com    | 9990001112 | P9999999    |\n+--------------+--------------+-----------------------+------------+-------------+")
    ]

    for filename, title, subtitle in screenshots:
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#1e293b')
        
        # Header banner
        ax.text(0.5, 0.82, title, color='#ffffff', fontsize=16, fontweight='bold', ha='center', va='center')
        ax.text(0.5, 0.45, subtitle, color='#93c5fd', fontsize=11, ha='center', va='center', family='monospace')
        
        # Decorative border box
        rect = plt.Rectangle((0.05, 0.08), 0.9, 0.84, fill=False, edgecolor='#38bdf8', linewidth=2, transform=ax.transAxes)
        ax.add_patch(rect)
        
        ax.axis('off')
        plt.tight_layout()
        filepath = os.path.join(target_dir, filename)
        plt.savefig(filepath, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        print(f"Generated screenshot mockup: {filename}")

if __name__ == "__main__":
    create_screenshot_assets()
