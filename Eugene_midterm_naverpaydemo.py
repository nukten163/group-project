import sys
import math
import random


def register_account(user):
    bank = input("은행명을 입력하세요: ")
    account_number = input("계좌번호를 입력하세요: ")
    if user['account'] and user['account']['number'] == account_number:
        print("동일한 계좌가 이미 등록되어 있습니다.")
    else:
        user['account'] = {'bank': bank, 'number': account_number}
        print("계좌가 등록되었습니다.")
    main_menu(user)


def verify_account(user):
    if not user['account']:
        register_account(user)
    return True


def charge_balance(user, amount):
    user['balance'] += amount
    print(f"충전 완료. 현재 잔액은 {user['balance']}원입니다.")


def ensure_balance(user, amount):
    while user['balance'] < amount:
        needed = math.ceil((amount - user['balance']) / 1000) * 1000
        print(f"필요한 금액은 {needed}원입니다.")
        amount = int(input("충전할 금액을 입력하세요: "))
        while amount < needed:
            print("충전할 금액이 부족합니다.")
            amount = int(input('충전할 금액을 입력하세요: '))
        charge_balance(user, amount)
    return amount


def transfer(user, amount, recipient_name, recipient_bank, recipient_account):
    if input('저장할까요? (y/n): ') == 'y':
        nickname = input('닉네임을 입력하세요: ')
        if not nickname:
            nickname = len(user['saved_accounts'])
        user['saved_accounts'][nickname] = (recipient_name, recipient_bank, recipient_account)
        print('저장되었습니다.')
    user['balance'] -= amount
    print(f"송금이 완료되었습니다. 남은 잔액은 {user['balance']}원입니다.")
    main_menu(user)


def prompt_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("유효한 숫자를 입력해 주세요.")


def check_balance(user):
    if not user['account']:
        print("계좌가 존재하지 않습니다. 지금 계좌를 등록해서 계좌 및 포인트를 조회하세요!")
        noaccountchoice = input('1. 계좌 등록하기\n2. 메인 메뉴로 돌아가기\n선택: ')
        if noaccountchoice == '1':
            register_account(user)
        elif noaccountchoice == '2':
            main_menu(user)
            return

    elif user['balance'] == 0:
        print('잔액이 없습니다. 충전하시겠습니까?')
        nobalancechoice = input('1. 충전하기\n2. 메인 메뉴로 돌아가기\n선택: ')
        if nobalancechoice == '1':
            charge_balance_menu(user)
        elif nobalancechoice == '2':
            main_menu(user)
            return

    print(f"\n이름: {user['name']}")
    print(f"잔액: {user['balance']}원")
    print(f"등록 계좌: {user['account'] if user['account'] else '없음'}")
    print(f"보유포인트: {user['points']}p")
    main_menu(user)


def charge_balance_menu(user):
    if not user['account']:
        print('계좌가 존재하지 않습니다.')
        register_account(user)
    amount = prompt_integer("충전할 금액을 입력하세요: ")
    charge_balance(user, amount)
    main_menu(user)


def transfer_menu(user):
    if not user['account']:
        print('계좌가 존재하지 않아 송금이 불가합니다.')
        register_account(user)
    amount = prompt_integer("송금할 금액을 입력하세요: ")
    ensure_balance(user, amount)
    recipient_name = input("송금 받을 사람의 이름: ")
    recipient_bank = input("송금 받을 사람의 은행명: ")
    recipient_account = input("송금 받을 사람의 계좌번호: ")
    transfer(user, amount, recipient_name, recipient_bank, recipient_account)


def pay(user):
    if not user['account']:
        print('계좌가 등록되지 않아 결제가 불가합니다.')
        register_account(user)
    amount = prompt_integer("결제할 금액을 입력하세요: ")
    ensure_balance(user, amount)
    recheck = input(f'결제하시겠습니까? 결제 금액은 {amount}, 적립은 {int(float(amount) * 0.05)}원입니다. (y/n): ')
    if recheck.lower() == 'y':
        user['balance'] -= amount
        user['points'] += int(float(amount) * 0.05)
        print('결제가 완료되었습니다.')
        print(f'잔액은 {user['balance']}원입니다.')
        print(f'적립 포인트: {user['points']}p, 보유 포인트: {user['points']}p')
        addpointyn = input('추가 포인트를 적립하시겠습니까? (y/n): ')
        if addpointyn.lower() == 'y':
            addpoint = input('임의의 숫자를 입력해주세요...')
            random_point = random.randint(1, 100)
            print(f'축하합니다! {addpoint} 선택 결과 {random_point}p가 추가되었습니다.')
            user['points'] += random_point
        elif addpointyn.lower() == 'n':
            print('메인 메뉴로 돌아갑니다.')
    elif recheck.lower() == 'n':
        main_menu(user)
        return
    main_menu(user)


def validate_gift_card_number(card_number):
    import re
    pattern = re.compile(r'^[a-zA-Z]-\d{4}-\d{4}-\d{3}$')
    return bool(pattern.match(card_number))


def register_gift_card(user):
    while True:
        try:
            card_number = input("기프트카드 번호를 입력하세요 (예: a-1234-5678-901): ")
            if card_number.lower() == 'q':
                print('메인 메뉴로 돌아갑니다.')
                main_menu(user)
                return
            elif validate_gift_card_number(card_number):
                prefix = card_number.split('-')[0].lower()
                amount_map = {'p': 50000, 'q': 30000, 'r': 10000}
                amount = amount_map.get(prefix, 5000)
                print(f"이 기프트카드로 {amount}원이 충전됩니다.")
                confirm = input("등록을 진행하시겠습니까? (y/n): ")
                if confirm.lower() == 'y':
                    charge_balance(user, amount)
                    print(f"기프트카드 등록 완료. 현재 잔액은 {user['balance']}원입니다.")
                    break
                else:
                    print("기프트카드 등록이 취소되었습니다.")
                    break
            else:
                print("잘못된 기프트카드 번호 형식입니다. 올바른 형식으로 입력해주세요.")
        except UnicodeDecodeError:
            print("입력 인코딩에 문제가 발생했습니다. 다시 입력해주세요.")
    main_menu(user)


def main_menu(user):
    print("\n메인 메뉴")
    print("1. 잔액 확인")
    print("2. 충전하기")
    print("3. 송금하기")
    print("4. 결제하기")
    print("5. 기프트카드 등록하기")
    print("0. 프로그램 종료")
    choice = input("선택: ")
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
        print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
        sys.exit()


def main():
    print("프로그램을 시작합니다. 사용자의 이름을 입력하세요.")
    user_name = input("이름: ")
    user = {
        'name': user_name,
        'balance': 0,
        'account': None,
        'points': 0,
        'saved_accounts': {}
    }
    print(f'환영합니다, {user_name}님!')
    main_menu(user)


if __name__ == "__main__":
    main()
