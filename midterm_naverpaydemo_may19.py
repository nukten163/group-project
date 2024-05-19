import sys
import math
import random
import string
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
        print(f'All {user["name"]} activity: \n')
        print(tabulate(user["activity_log"], headers=['Date', 'Account', 'Operation', 'Balance', 'Point']))
    main_menu()

def register_account(user):
    """ Save bank name and account number in user's <accounts> dictionary """
    print("\nRegister your account.\n")
    bank = input("Enter bank name >> ").strip()
    account_number = input("Enter account number >> ").strip()
    if user['account'] and user['account']['number'] == account_number:
        print("The same account is already registered.")
    else:
        user['account'] = {'bank': bank, 'number': account_number}
        add_operation(user, 'Account Registered')
        print("The account has been registered.")
    main_menu()

def verify_account(user):
    """ Varify if user has had any accounts registered """
    if not user['account']:
        register_account(user)
    return True

def charge_balance(user, amount):
    """ Top up pay money """
    user['balance'] += amount
    add_operation(user, 'Balance is charged')
    print(f"Charge complete. Current balance is: {user['balance']}.")

def ensure_balance(user, amount):
    """ Calculate the amount to be charged when the balance is not enough to send or pay """
    while user['balance'] < amount:
        needed = math.ceil((amount - user['balance']) / 1000) * 1000
        print(f"The required amount is: {needed}.")
        amount = int(input("Enter the amount to charge >> ").strip())
        while amount < needed:
            print("The amount to charge is insufficient.")
            amount = int(input("Enter the amount to charge >> ").strip())
        charge_balance(user, amount)
    return amount

def transfer(user, amount, recipient_name, recipient_bank, recipient_account):
     """ Send Money and save the recipient's bank account with alias """
    if input("Do you want to save it? [ Y / N ] >> ").strip().lower() == 'y':
        nickname = input("Enter a nickname >> ").strip()
        if not nickname:
            nickname = len(user['saved_accounts'])
        user['saved_accounts'][nickname] = (recipient_name, recipient_bank, recipient_account)
        print('Saved.')
    user['balance'] -= amount
    add_operation(user, 'Transfer')
    print(f"Transfer complete. Remaining balance is: {user['balance']}.")
    main_menu()

def prompt_integer(prompt):
    """ Filter out wrong inputs """
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")

def check_balance(user):
    """ Check My Naver Pay status  """
    if not user['account']:
        print("No account exists. Register an account now to check balance and points!")
        noaccountchoice = input("1. Register account\n2. Return to main menu\nSelect >> ").strip().lower()
        if noaccountchoice == '1':
            register_account(user)
        elif noaccountchoice == '2':
            main_menu()
            return

    elif user['balance'] == 0:
        print('No balance. Do you want to charge?')
        nobalancechoice = input("1. Charge\n2. Return to main menu\nSelect >> ").strip().lower()
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
    """ Charge balance after checking if the user has a registered account and filtering out wrong inputs """
    if not user['account']:
        print('No account exists.')
        register_account(user)
    amount = prompt_integer("Enter the amount to charge >> ")
    charge_balance(user, amount)
    main_menu()

def transfer_menu(user):
    """ Transfer money after checking if the user has a registered account and filtering out wrong inputs """
    if not user['account']:
        print('Cannot transfer without an account.')
        register_account(user)
    amount = prompt_integer("Enter the amount to transfer >> ")
    ensure_balance(user, amount)
    recipient_name = input("Recipient's name >> ").strip()
    recipient_bank = input("Recipient's bank >> ").strip()
    recipient_account = input("Recipient's account number >> ").strip()
    transfer(user, amount, recipient_name, recipient_bank, recipient_account)
    add_operation(user, 'Transfer')

def pay(user):
     """ Pay after checking if the user has a registered account and filtering out wrong inputs  """
    if not user['account']:
        print('Cannot make payments without a registered account.')
        register_account(user)
    amount = prompt_integer("Enter the amount to pay >> ")
    ensure_balance(user, amount)

    alias = input("Enter an alias for the payment (optional) >> ").strip()
    transportation_list = ["bus", "taxi", "train", "subway"]
    bonus_points = 0

    if alias:
        if alias.lower() in transportation_list:
            bonus_points = int(amount * 0.01)
            user['points'] += bonus_points
            print(f"Bonus points for transportation: {bonus_points}p")
        else:
            is_transportation = input(f'Is "{alias}" related to transportation? [ Y / N ] >> ').strip().lower()
            if is_transportation == 'y':
                transportation_list.append(alias.lower())
                bonus_points = int(amount * 0.01)
                user['points'] += bonus_points
                print(f"Alias added to transportation list. Bonus points: {bonus_points}p")
                print("Warning: In case of perjury, the points will be forfeited.")

    recheck = input(f'Do you want to proceed with the payment? The payment amount is: {amount}, and the points earned are: {int(float(amount) * 0.05) + bonus_points}p. [ Y / N ] >> ').strip().lower()
    if recheck == 'y':
        user['balance'] -= amount
        user['points'] += int(float(amount) * 0.05)
        print('Payment complete.')
        print(f"Remaining balance is: {user['balance']}.")
        print(f"Points earned: {user['points']}p, Total points: {user['points']}p")
        addpointyn = input('Do you want to earn additional points? [ Y / N ] >> ').strip().lower()
        if addpointyn == 'y':  # Roulette for extra random points
            colors = ["red", "blue", "purple", "green", "yellow", "pink"]
            color_initials = {color[0]: color for color in colors}
            numbers = random.sample([i for i in range(1, 11)], 6)
            roulette = {color: number for color, number in zip(colors, numbers)}  # Assign each color to random numbers between 1~10

            chosen_color_initial = input(f"Roulette Board: {', '.join([color[0] for color in colors])}\nChoose one color >> ").strip().lower()
            if chosen_color_initial in color_initials:
                chosen_color = color_initials[chosen_color_initial]
                random_points = roulette[chosen_color]
                print(f'Congratulations! Your selection of {chosen_color} resulted in: {random_points} additional points.')
                user['points'] += random_points
                print(f"Current points: {user['points']}p")
            else:
                print("Invalid color choice.")
        elif addpointyn == 'n':
            print('Returning to the main menu.')
    elif recheck == 'n':
        main_menu()
        return

    add_operation(user, 'Payment')
    main_menu()

def validate_gift_card_number(card_number):
    """ Filter out wrong gift cards """
    import re
    pattern = re.compile(r'^[a-zA-Z]-\d{4}-\d{4}-\d{3}$')
    return bool(pattern.match(card_number))

def register_gift_card(user):
    """ register giftcard and add money from it """
    while True:
        try:
            card_number = input("Enter the gift card number (e.g., a-1234-5678-901) >> ").strip()
            if card_number.lower() == 'q':
                print('Returning to the main menu.')
                main_menu()
                return
            elif validate_gift_card_number(card_number):
                prefix = card_number.split('-')[0].lower()
                amount_map = {'p': 50000, 'q': 30000, 'r': 10000}
                amount = amount_map.get(prefix, 5000)
                print(f"This gift card will charge: {amount}.")
                confirm = input("Do you want to proceed with the registration? [ Y / N ] >> ").strip().lower()
                if confirm == 'y':
                    charge_balance(user, amount)
                    print(f"Gift card registration complete. Current balance is: {user['balance']}.")
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

def generate_gift_card_number(amount):
    """Create gift card number"""
    if amount == 50000:
        char_part = 'p'
    elif amount == 30000:
        char_part = 'q'
    elif amount == 10000:
        char_part = 'r'
    else:
        char_part = random.choice([ch for ch in string.ascii_lowercase if ch not in 'pqr'])

    digit_part = '-'.join(
        ''.join(random.choices(string.digits, k=size)) for size in [4, 4, 3]
    )
    return f"{char_part}-{digit_part}"

def buy_gift_card(user):
    """Let the user buy gift card"""
    while True:
        print("Choose the gift card amount:")
        print("1. 50000")
        print("2. 30000")
        print("3. 10000")
        print("4. 5000")
        choice = input("Select >> ").strip().lower()
        amount_map = {'1': 50000, '2': 30000, '3': 10000, '4': 5000}

        if choice in amount_map:
            amount = amount_map[choice]
            if amount > user['balance']:
                print(f"Insufficient balance. Current balance is: {user['balance']}.")
                insufficient_choice = input("1. Top Up\n2. Return to home screen\nSelect >> ").strip().lower()
                if insufficient_choice == '1':
                    charge_balance_menu(user)
                elif insufficient_choice == '2':
                    main_menu()
                return
            user['balance'] -= amount
            gift_card_number = generate_gift_card_number(amount)
            print(f"Gift card purchase complete. Gift card number: {gift_card_number}")
            print(f"Current balance is: {user['balance']}.")
            break
        else:
            print("Invalid choice. Please try again.")
    add_operation(user, f'Gift card purchased: {gift_card_number}')
    main_menu()

def create_menu(options):
    """ Show the main menu and let the user make a choice """
    def menu():
        print("\nMain Menu")
        for key, value in options.items():
            print(f"{key}. {value['description']}")
        choice = input("Select an option >> ").strip().lower()
        if choice in options:
            print(f"Moving to {options[choice]['description']}...\n")
            options[choice]['function']()  # Execute the function
        else:
            print("Invalid option, please try again.")
            menu()  # show the menu again if invalid input
    return menu

def setup_main_menu(user):
    options = {
        '1': {'description': 'check your status', 'function': lambda: check_balance(user)},
        '2': {'description': 'top up', 'function': lambda: charge_balance_menu(user)},
        '3': {'description': 'send money', 'function': lambda: transfer_menu(user)},
        '4': {'description': 'make a payment', 'function': lambda: pay(user)},
        '5': {'description': 'register a gift card', 'function': lambda: register_gift_card(user)},
        '6': {'description': 'buy a gift card', 'function': lambda: buy_gift_card(user)},
        '7': {'description': 'see all activity', 'function': lambda: all_activity(user)},
        '0': {'description': 'quit', 'function': lambda: sys.exit()}
    }
    return create_menu(options)

def main():
    """ User log-in + Welcome """
    print("Starting the program. Please enter the user's name.")
    user_name = input("Name >> ").strip().title()
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
    """ Get the program started """
    main()