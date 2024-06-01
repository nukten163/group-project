import csv
import os
import pandas as pd
from datetime import datetime, timedelta

# Define file paths
USERS_CSV = 'users.csv'
RESERVATIONS_CSV = 'reservations.csv'

# Define room divisions and prices
room_division = {
    'standard': [201, 202, 203, 204, 205],
    'deluxe': [301, 302, 303],
    'suite': [401, 402]
}

room_prices = {
    'standard': 100,
    'deluxe': 150,
    'suite': 200
}

class Promotion: #### just filled in this class so that it won't get any error when running.. yujin will make this part later
    @staticmethod
    def get_promotion_discount(promotion_id):
        return 10  # Example: return 10% discount for any promotion ID

class Documentation:
    @staticmethod
    def initialize_csv():
        if not os.path.exists(USERS_CSV):
            with open(USERS_CSV, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['UserID', 'UserName', 'Email', 'Phone', 'Preferences', 'Requirements'])

        if not os.path.exists(RESERVATIONS_CSV):
            with open(RESERVATIONS_CSV, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ReservationID', 'UserID', 'RoomNumber', 'CheckInDate', 'CheckOutDate', 'OrderDate'])

class Customer:
    def __init__(self, user_id, user_name, email=None, phone=None, preferences=None, requirements=None):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.phone = phone
        self.preferences = preferences if preferences else []
        self.requirements = requirements if requirements else []

    def __repr__(self):
        return f"Customer(UserID={self.user_id}, Name={self.user_name}, Email={self.email}, Phone={self.phone}, Preferences={self.preferences}, Requirements={self.requirements})"

    @staticmethod
    def add_user(user_id, user_name, email, phone, preferences='', requirements=''):
        with open(USERS_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, user_name, email, phone, preferences, requirements])

    @staticmethod
    def create_invoice(reservation): ####### I moved the invoice function into Customer class!!!!
        invoice = f"""
        ================Invoice==============

        Reservation ID: {reservation.reservation_id}
        Customer: {reservation.customer.user_name}
        Room Number: {reservation.room_number}
        Check-in Date: {reservation.check_in_date}
        Order Date: {reservation.order_date}

        ======================================
        """
        print(invoice)
        return invoice

    @staticmethod
    def email_invoice(invoice):
        print("Emailing Invoice...")
        print(invoice)

class Reservation:
    def __init__(self, reservation_id, room_number, customer, check_in_date, check_out_date, order_date):
        self.reservation_id = reservation_id
        self.room_number = room_number
        self.customer = customer
        self.check_in_date = pd.to_datetime(check_in_date)
        self.check_out_date = pd.to_datetime(check_out_date)
        self.order_date = pd.to_datetime(order_date)
        self.arrival_time = None
        self.mobile_key = None
        self.billing_info = None

    def self_check_in(self): ##### self check in ===> print out the information so that customer can confirm
        num_nights = (self.check_out_date - self.check_in_date).days
        print(f"Reservation Number: {self.reservation_id}")
        print(f"Hotel Name: The PLAZA Hotel")
        print(f"Check-in Date: {self.check_in_date.strftime('%Y-%m-%d')}")
        print(f"Number of Nights: {num_nights}")
        print(f"Room Type: {data_manager.get_room_type(self.room_number)}")
        print(f"Bed Type: {data_manager.get_bed_type(self.room_number)}")

        # Additional self check-in details
        self.arrival_time = input("Enter your arrival time (HH:MM): ")
        self.mobile_key = input("Would you like to receive a mobile key? (yes/no): ")
        self.billing_info = input("Enter your billing information (credit card information): ")

    def check_in(self, self_check_in=False):  ############ Normal check in at hotel
        if self_check_in:
            # Check if self-check-in is allowed (within 24 hours)
            if datetime.now() < self.check_in_date - timedelta(days=1):
                print("Self check-in is only available within 24 hours before the check-in date.")
                return

            self.self_check_in()

        print(f"{self.customer.user_name} has checked into room {self.room_number}.")
    
    @staticmethod
    def add_reservation(reservation_id, user_id, room_number, reservation_date, order_date):
        with open(RESERVATIONS_CSV, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([reservation_id, user_id, room_number, reservation_date, order_date])

    @staticmethod
    def view_reservations():
        with open(RESERVATIONS_CSV, 'r') as file:
            reservation_reader = csv.reader(file)
            next(reservation_reader)  # Skip header row
            reservations = list(reservation_reader)

        with open(USERS_CSV, 'r') as file:
            user_reader = csv.reader(file)
            next(user_reader)  # Skip header row
            users = {rows[0]: rows[1] for rows in user_reader}

        for reservation in reservations:
            reservation_id, user_id, room_number, reservation_date, order_date = reservation
            user_name = users.get(user_id, 'Unknown User')
            print(f"ReservationID: {reservation_id}, User: {user_name}, Room: {room_number}, Reservation Date: {reservation_date}, Order Date: {order_date}")

    @staticmethod
    def cancel_reservation(reservation_id):
        rows = []
        with open(RESERVATIONS_CSV, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] != reservation_id:
                    rows.append(row)

        with open(RESERVATIONS_CSV, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

    @staticmethod
    def view_user_reservations(user_id):
        with open(RESERVATIONS_CSV, 'r') as file:
            reservation_reader = csv.reader(file)
            next(reservation_reader)  # Skip header row
            user_reservations = [row for row in reservation_reader if row[1] == user_id]

        with open(USERS_CSV, 'r') as file:
            user_reader = csv.reader(file)
            next(user_reader)  # Skip header row
            users = {rows[0]: rows[1] for rows in user_reader}

        user_name = users.get(user_id, 'Unknown User')
        print(f"Reservations for {user_name} (UserID: {user_id}):")
        for reservation in user_reservations:
            reservation_id, user_id, room_number, reservation_date, order_date = reservation
            print(f"  ReservationID: {reservation_id}, Room: {room_number}, Reservation Date: {reservation_date}, Order Date: {order_date}")

class DataManager:
    def __init__(self, df):
        self.df = df
        self.reservations = []
        self.customers = []

        # Initialize availability
        date_columns = self.df.columns[2:]  # All date columns
        for date_column in date_columns:
            self.df[date_column].fillna('Available', inplace=True)

    def add_reservation(self, reservation):
        self.reservations.append(reservation)
        self.update_excel(reservation)

    def add_customer(self, customer):
        self.customers.append(customer)

    def find_reservation(self, reservation_id, customer_name):
        result = False
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id and reservation.customer.user_name == customer_name:
                result = reservation
        return result
            

    def find_customer(self, membership_number):
        result = False
        for customer in self.customers:
            if customer.membership_number == membership_number:
                result = customer
        return result

    def get_room_type(self, room_number):
        room_info = self.df.loc[self.df['room number'] == room_number]
        if not room_info.empty:
            return room_info['type'].values[0]
        return "Unknown"

    def get_bed_type(self, room_number):
        room_type = self.get_room_type(room_number)
        if room_type == 'standard':
            return '1 Queen Bed or 2 Twin Beds'
        elif room_type == 'deluxe':
            return '1 King Bed + 1 Twin Bed or 1 Queen Bed + 1 Twin Bed'
        elif room_type == 'suite':
            return '2 Queen Beds or 1 King Bed + 1 Sofa Bed'
        return 'Configuration Not Available'

    def update_excel(self, reservation):
        check_in_date = reservation.check_in_date.strftime('%Y-%m-%d')
        room_number = reservation.room_number
        reservation_id = reservation.reservation_id

        if room_number in self.df['room number'].values:
            self.df.loc[self.df['room number'] == room_number, 'availability'] = reservation_id

    def to_dataframe(self):
        return self.df

def check_in(customer_name, reservation_id, self_check_in=False):
    reservation = data_manager.find_reservation(reservation_id, customer_name)
    if not reservation:
        print(f"No reservation found for {customer_name} with reservation number {reservation_id}.")
        return
    
    reservation.check_in(self_check_in=self_check_in)

def load_data(file_name):
    df = pd.read_excel(file_name)
    return df

def save_data(df, file_name):
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, index=False)

# Initialize CSVs if not present
Documentation.initialize_csv()

# Load and manage hotel room data
hotel_data = load_data('HotelRoomData.xlsx')
data_manager = DataManager(hotel_data)

############################################   TEST   #############################################
# Example usage
customer1 = Customer("1", "John Doe")
customer2 = Customer("2", "Jane Smith")
data_manager.add_customer(customer1)
data_manager.add_customer(customer2)

# Adding reservations
reservation1 = Reservation(1234567891, 201, customer1, '2024-12-01', '2024-12-02', '2024-05-31')
reservation2 = Reservation(7654321890, 202, customer2, '2024-12-03', '2024-12-05', '2024-05-26')
reservation3 = Reservation(1357910123, 303, customer1, '2024-12-05', '2024-12-06', '2024-06-01')
data_manager.add_reservation(reservation1)
data_manager.add_reservation(reservation2)
data_manager.add_reservation(reservation3)

# Check-in TEST!!!!!!!! ***
check_in("John Doe", 1234567891, self_check_in=True)  # Self check-in
check_in("Jane Smith", 7654321890)  # Normal check-in at hotel

# Save the updated state to Excel
updated_df = data_manager.to_dataframe()
save_data(updated_df, 'HotelRoomData.xlsx')

# Display updated hotel data
print("Updated hotel data:")
print(updated_df)

print("All reservations:")
for reservation in data_manager.reservations:
    print(f"Reservation ID: {reservation.reservation_id}, Room: {reservation.room_number}, Check-in: {reservation.check_in_date}, Check-out: {reservation.check_out_date}, Order Date: {reservation.order_date}")
