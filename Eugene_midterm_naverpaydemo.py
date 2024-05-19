import sys
import math
import random
from tabulate import tabulate
import datetime

today = str(datetime.date.today())

def add_operation(user, message: str):
    balance = user['balance']
    points = user['points']
    user['activity_log'].append([today, user['account'], message, balance, points])

def all_activity(user):
    if len(user['activity_log']) == 0:
        print('No activity detected')
    else:
        print(f'All {user["name"]} activity: ')
        print(tabulate(user["activity_log"], headers=['Date', 'Account', 'Operation', 'Balance', 'Point']))
    main_menu()

def register_account(user):
    bank = input("Enter bank name: ")
    account_number = input("Enter account number: ")
    if user['account'] and user['account']['number'] == account_number:
        print("The same account is already registered.")
    else:
        user['account'] = {'bank': bank, 'number': account_number}
        add_operation(user, 'Account Registered')
        print("The account has been registered.")
    main_menu()

def verify_account(user):
    if not user['account']:
        register_account(user)
    return True

def charge_balance(user, amount):
    user['balance'] += amount
    add_operation(user, 'Balance is charged')
    print(f"Charge complete. Current balance is {user['balance']}.")

def ensure_balance(user, amount):
    while user['balance'] < amount:
        needed = math.ceil((amount - user['balance']) / 1000) * 1000
        print(f"The required amount is {needed}.")
        amount = int(input("Enter the amount to charge: "))
        while amount < needed:
            print("The amount to charge is insufficient.")
            amount = int(input('Enter the amount to charge: '))
        charge_balance(user, amount)
    return amount

def transfer(user, amount, recipient_name, recipient_bank, recipient_account):
    if input('Do you want to save it? (y/n): ') == 'y':
        nickname = input('Enter a nickname: ')
        if not nickname:
            nickname = len(user['saved_accounts'])
        user['saved_accounts'][nickname] = (recipient_name, recipient_bank, recipient_account)
        print('Saved.')
    user['balance'] -= amount
    add_operation(user, 'Transfer')
    print(f"Transfer complete. Remaining balance is {user['balance']}.")
    main_menu()

def prompt_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def check_balance(user):
    if not user['account']:
        print("No account exists. Register an account now to check balance and points!")
        noaccountchoice = input('1. Register account\n2. Return to main menu\nSelect: ')
        if noaccountchoice == '1':
            register_account(user)
        elif noaccountchoice == '2':
            main_menu()
            return

    elif user['balance'] == 0:
        print('No balance. Do you want to charge?')
        nobalancechoice = input('1. Charge\n2. Return to main menu\nSelect: ')
        if nobalancechoice == '1':
            charge_balance_menu(user)
        elif nobalancechoice == '2':
            main_menu()
            return

    print(f"\nName: {user['name']}")
    print(f"Balance: {user['balance']}")
    print(f"Registered account: {user['account'] if user['account'] else 'None'}")
    print(f"Points: {user['points']}p")
    main_menu()

def charge_balance_menu(user):
    if not user['account']:
        print('No account exists.')
        register_account(user)
    amount = prompt_integer("Enter the amount to charge: ")
    charge_balance(user, amount)
    main_menu()

def transfer_menu(user):
    if not user['account']:
        print('Cannot transfer without an account.')
        register_account(user)
    amount = prompt_integer("Enter the amount to transfer: ")
    ensure_balance(user, amount)
    recipient_name = input("Recipient's name: ")
    recipient_bank = input("Recipient's bank: ")
    recipient_account = input("Recipient's account number: ")
    transfer(user, amount, recipient_name, recipient_bank, recipient_account)
    add_operation(user, 'Transfer')

def pay(user):
    if not user['account']:
        print('Cannot make payments without a registered account.')
        register_account(user)
    amount = prompt_integer("Enter the amount to pay: ")
    ensure_balance(user, amount)
    recheck = input(f'Do you want to proceed with the payment? The payment amount is {amount}, and the points earned are {int(float(amount) * 0.05)}p. (y/n): ')
    if recheck.lower() == 'y':
        user['balance'] -= amount
        user['points'] += int(float(amount) * 0.05)
        print('Payment complete.')
        print(f"Remaining balance is {user['balance']}.")
        print(f"Points earned: {user['points']}p, Total points: {user['points']}p")
        addpointyn = input('Do you want to earn additional points? (y/n): ')
        if addpointyn.lower() == 'y':
            addpoint = input('Enter any number...')
            random_point = random.randint(1, 100)
            print(f'Congratulations! Your selection of {addpoint} resulted in {random_point} additional points.')
            user['points'] += random_point
        elif addpointyn.lower() == 'n':
            print('Returning to the main menu.')
    elif recheck.lower() == 'n':
        main_menu()
        return

    add_operation(user, 'Payment')
    main_menu()


def validate_gift_card_number(card_number):
    import re
    pattern = re.compile(r'^[a-zA-Z]-\d{4}-\d{4}-\d{3}$')
    return bool(pattern.match(card_number))


def register_gift_card(user):
    while True:
        try:
            card_number = input("Enter the gift card number (e.g., a-1234-5678-901): ")
            if card_number.lower() == 'q':
                print('Returning to the main menu.')
                main_menu()
                return
            elif validate_gift_card_number(card_number):
                prefix = card_number.split('-')[0].lower()
                amount_map = {'p': 50000, 'q': 30000, 'r': 10000}
                amount = amount_map.get(prefix, 5000)
                print(f"This gift card will charge {amount}.")
                confirm = input("Do you want to proceed with the registration? (y/n): ")
                if confirm.lower() == 'y':
                    charge_balance(user, amount)
                    print(f"Gift card registration complete. Current balance is {user['balance']}.")
                    break
                else:
                    print("Gift card registration canceled.")
                    break
            else:
                print("Invalid gift card number format. Please enter in the correct format.")
        except UnicodeDecodeError:
            print("Input encoding issue. Please try again.")
    add_operation(user, 'Gift card created')
    main_menu()

def create_menu(options):
    def menu():
        print("\nMain Menu")
        for key, value in options.items():
            print(f"{key}. {value['description']}")
        choice = input("Select an option: ")
        if choice in options:
            options[choice]['function']()  # Execute the function
        else:
            print("Invalid option, please try again.")
            menu()  # show the menu again if invalid input
    return menu

def setup_main_menu(user):
    options = {
        '1': {'description': 'Check My Status', 'function': lambda: check_balance(user)},
        '2': {'description': 'Top Up', 'function': lambda: charge_balance_menu(user)},
        '3': {'description': 'Send Money', 'function': lambda: transfer_menu(user)},
        '4': {'description': 'Pay', 'function': lambda: pay(user)},
        '5': {'description': 'Register Gift Card', 'function': lambda: register_gift_card(user)},
        '6': {'description': 'See All Activity', 'function': lambda: all_activity(user)},
        '0': {'description': 'Quit', 'function': lambda: sys.exit()}
    }
    return create_menu(options)

def main():
    print("Starting the program. Please enter the user's name.")
    user_name = input("Name: ")
    user = {
        'name': user_name,
        'balance': 0,
        'account': None,
        'points': 0,
        'saved_accounts': {},
        'activity_log': []
    }
    print(f'Welcome, {user_name}!')
    global main_menu
    main_menu = setup_main_menu(user)
    main_menu()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
