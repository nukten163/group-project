
import csv
import os
import pandas as pd

USERS_CSV = 'users.csv'
RESERVATIONS_CSV = 'reservations.csv'

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
                writer.writerow(['ReservationID', 'UserID', 'RoomNumber', 'ReservationDate', 'OrderDate'])

    @staticmethod
    def create_invoice(reservation):
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

class Reservation:
    def __init__(self, reservation_id, room_number, customer, check_in_date, order_date):
        self.reservation_id = reservation_id
        self.room_number = room_number
        self.customer = customer
        self.check_in_date = check_in_date
        self.order_date = order_date

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

    def find_reservation(self, room_number):
        for reservation in self.reservations:
            if reservation.room_number == room_number:
                return reservation
        return None

    def find_customer(self, membership_number):
        for customer in self.customers:
            if customer.membership_number == membership_number:
                return customer
        return None

    def update_excel(self, reservation):
        check_in_date = reservation.check_in_date
        room_number = reservation.room_number
        reservation_id = reservation.reservation_id

        if room_number in self.df['room number'].values:
            self.df.loc[self.df['room number'] == room_number, check_in_date] = reservation_id

    def to_dataframe(self):
        return self.df

def load_data(file_name):
    df = pd.read_excel(file_name)
    return df

def save_data(df, file_name):
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, index=False)

# Simulate HotelRoomData.xlsx
hotel_room_data = {
    'room number': [101, 102, 103, 104],
    'type': ['Single', 'Double', 'Suite', 'Single'],
    'Dec 1': ['Available', 'Available', 'Available', 'Available'],
    'Dec 3': ['Available', 'Available', 'Available', 'Available'],
    'Dec 5': ['Available', 'Available', 'Available', 'Available']
}

# Create DataFrame
hotel_data_df = pd.DataFrame(hotel_room_data)

# Initialize DataManager with the hotel data
data_manager = DataManager(hotel_data_df)

# Example usage
customer1 = Customer("John Doe", "1")
customer2 = Customer("Jane Smith", "2")
data_manager.add_customer(customer1)
data_manager.add_customer(customer2)

# Adding reservations
reservation1 = Reservation(1234567, 101, customer1, 'Dec 1', '2024-05-25')
reservation2 = Reservation(7654321, 102, customer2, 'Dec 3', '2024-05-26')
reservation3 = Reservation(1357910, 103, customer1, 'Dec 5', '2024-06-01')
data_manager.add_reservation(reservation1)
data_manager.add_reservation(reservation2)
data_manager.add_reservation(reservation3)

# Save the updated state to Excel
updated_df = data_manager.to_dataframe()
output_path = 'HotelRoomData.xlsx'
save_data(updated_df, output_path)

print("Updated hotel data:")
print(updated_df)

print("All reservations:")
Reservation.view_reservations()
