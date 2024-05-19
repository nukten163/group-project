import sys
import math
import random


def register_account(user):
    #docstring => ''' explanation of each function ''' (remove this comment when submitting)
    """ Save bank name and account number in user's <accounts> dictionary """

    bank = input("Enter bank name: ")
    account_number = input("Enter account number: ")
    
    if user['account'] and user['account']['number'] == account_number:
        print("The same account is already registered.")
    else:
        user['account'] = {'bank': bank, 'number': account_number}
        print("The account has been registered.")
    main_menu(user)


def verify_account(user):
    """ Varify if user has had any accounts registered """
    if not user['account']:
        register_account(user)
    return True


def charge_balance(user, amount):
    """ Top up pay money """
    user['balance'] += amount
    print(f"Charge complete. Current balance is {user['balance']}.")


def ensure_balance(user, amount):
    """ Calculate the amount to be charged when the balance is not enough to send or pay """
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
    """ Send Money and save the recipient's bank account with alias """

    if input('Do you want to save it? (y/n): ') == 'y':

        '''Save the recipient's account like following form in the <saved_accounts> dictionary
        => { Jisoo : [Woori, 123456] } '''

        user['saved_accounts'][recipient_name] = [recipient_bank, recipient_account] 

        # Make alias
        alias = input("Wish to make alias?[y/n] ")
        if alias == 'y':
            alias = input("Save as>> ")
            user['saved_accounts'][recipient_name].append(alias)

        print('Saved.')

    user['balance'] -= amount
    print(f"Transfer complete. Remaining balance is {user['balance']}.")
    main_menu(user)


def prompt_integer(prompt):
    """ Filter out wrong inputs """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def check_balance(user):
    """ Check My Naver Pay status  """
    if not user['account']:
        print("No account exists. Register an account now to check balance and points!")
        noaccountchoice = input('1. Register account\n2. Return to main menu\nSelect: ')
        if noaccountchoice == '1':
            register_account(user)
        elif noaccountchoice == '2':
            main_menu(user)
            return

    elif user['balance'] == 0:
        print('No balance. Do you want to charge?')
        nobalancechoice = input('1. Charge\n2. Return to main menu\nSelect: ')
        if nobalancechoice == '1':
            charge_balance_menu(user)
        elif nobalancechoice == '2':
            main_menu(user)
            return

    print(f"\nName: {user['name']}")
    print(f"Balance: {user['balance']}")
    print(f"Registered account: {user['account'] if user['account'] else 'None'}")
    print(f"Points: {user['points']}p")
    main_menu(user)


def charge_balance_menu(user):
    """ Charge balance after checking if the user has a registered account and filtering out wrong inputs """
    if not user['account']:
        print('No account exists.')
        register_account(user)
    amount = prompt_integer("Enter the amount to charge: ")
    charge_balance(user, amount)
    main_menu(user)


def transfer_menu(user):
    """ Transfer money after checking if the user has a registered account and filtering out wrong inputs """
    if not user['account']:
        print('Cannot transfer without an account.')
        register_account(user)
    amount = prompt_integer("Enter the amount to transfer: ")
    ensure_balance(user, amount)
    recipient_name = input("Recipient's name: ")
    recipient_bank = input("Recipient's bank: ")
    recipient_account = input("Recipient's account number: ")
    transfer(user, amount, recipient_name, recipient_bank, recipient_account)


def pay(user):
    """ Pay after checking if the user has a registered account and filtering out wrong inputs  """
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
        if addpointyn.lower() == 'y': ### Roulette for extra random points
            colors = ["red", "blue", "black", "green", "yellow", "pink"] 
            numbers = random.sample([i for i in range(1,11)],6)
            roulette = {color : number for color, number in zip(colors, numbers)} # I assigned each color to random numbers between 1~10

            chosen_color = input(f"Roulette Board :  {colors}\nChoose one color >>> "  ) # You're gonna choose one color from the {colors}

            random_points = roulette[chosen_color]
            print(f'Congratulations! Your selection of {chosen_color} resulted in {random_points} additional points.')
            user['points'] += random_points
        elif addpointyn.lower() == 'n':
            print('Returning to the main menu.')
    elif recheck.lower() == 'n':
        main_menu(user)
        return
    main_menu(user)


def validate_gift_card_number(card_number):
    """ Filter out wrong gift cards """
    import re
    pattern = re.compile(r'^[a-zA-Z]-\d{4}-\d{4}-\d{3}$')
    return bool(pattern.match(card_number))


def register_gift_card(user):
    """ register giftcard and add money from it """
    while True:
        try:
            card_number = input("Enter the gift card number (e.g., a-1234-5678-901): ")
            if card_number.lower() == 'q':
                print('Returning to the main menu.')
                main_menu(user)
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
    main_menu(user)


def main_menu(user):
    """ Show the main menu and let the user make a choice """

    print("\nMain Menu")
    print("1. Check balance")
    print("2. Charge balance")
    print("3. Transfer")
    print("4. Pay")
    print("5. Register gift card")
    print("0. Exit program")
    choice = input("Select: ")
    if choice == '1':
        check_balance(user)
    elif choice == '2':
        charge_balance_menu(user)
    elif choice == '3':
        transfer_menu(user)
    elif choice == '4':
        pay(user)
    elif choice == '5':
        register_gift_card(user)
    elif choice == '0':
        print("Exiting the program. Thank you for using it.")
        sys.exit()


def main():
    """ User log-in + Welcome """
    print("Starting the program. Please enter the user's name.")
    user_name = input("Name: ")
    user = {
        'name': user_name,
        'balance': 0,
        'account': None,
        'points': 0,
        'saved_accounts': {}
    }
    print(f'Welcome, {user_name}!')
    main_menu(user)


if __name__ == "__main__":
    """ Get the program started """
    main()
