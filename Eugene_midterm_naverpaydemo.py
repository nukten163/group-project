import sys
import math
import random


class User:

  def __init__(self, name):
    self.name = name
    self.balance = 0
    self.account = None
    self.points = 0
    self.saved_accounts = {}

  def register_account(self):
    bank = input("은행명을 입력하세요: ")
    account_number = input("계좌번호를 입력하세요: ")
    if self.account and self.account['number'] == account_number:
      print("동일한 계좌가 이미 등록되어 있습니다.")
    else:
      self.account = {'bank': bank, 'number': account_number}
      print("계좌가 등록되었습니다.")

  def verify_account(self):
    if not self.account:
      self.register_account()
    return True

  def charge_balance(self, amount):
    self.balance += amount
    print(f"충전 완료. 현재 잔액은 {self.balance}원입니다.")

  def ensure_balance(self, amount):
    while self.balance < amount:
      needed = math.ceil((amount - self.balance) / 1000) * 1000
      print(f"필요한 금액은 {needed}원입니다.")
      amount = int(input("충전할 금액을 입력하세요: "))
      while amount < needed:
        print ("충전할 금액이 부족합니다.")
        amount = int(input ('충전할 금액을 입력하세요: '))
      self.charge_balance(amount)
    return amount

  def transfer(self, amount, recipient_name, recipient_bank, recipient_account):
    if input('저장할까요? (y/n): ') == 'y':
        nickname = input('닉네임을 입력하세요: ')
        if not nickname:
            nickname = len(self.saved_accounts)
        self.saved_accounts[nickname] = (recipient_name, recipient_bank, recipient_account)
        print('저장되었습니다.')
    self.balance -= amount
    print(f"송금이 완료되었습니다. 남은 잔액은 {self.balance}원입니다.")


class MenuManager:

  def __init__(self, user):
    self.user = user

  def prompt_integer(self, prompt):
    while True:
      try:
        return int(input(prompt))
      except ValueError:
        print("유효한 숫자를 입력해 주세요.")

  def main_menu(self):
    while True:
      print("\n메인 메뉴")
      print("1. 잔액 확인")
      print("2. 충전하기")
      print("3. 송금하기")
      print("4. 결제하기")
      print("5. 기프트카드 등록하기")
      print("0. 프로그램 종료")
      choice = input("선택: ")
      if choice == '1':
        self.check_balance()
      elif choice == '2':
        self.charge_balance()
      elif choice == '3':
        self.transfer()
      elif choice == '4':
        self.pay()
      elif choice == '5':
        self.register_gift_card()
      elif choice == '0':
        print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
        sys.exit()

  # 1
  def check_balance(self):
    if not self.user.account:
      print("계좌가 존재하지 않습니다. 지금 계좌를 등록해서 계좌 및 포인트를 조회하세요!")
      noaccountchoice = input ('1. 계좌 등록하기\n2. 메인 메뉴로 돌아가기\n선택: ')
      if noaccountchoice == '1':
        self.user.register_account()
      elif noaccountchoice == '2':
        return

    elif self.user.balance == 0:
      print ('잔액이 없습니다. 충전하시겠습니까?')
      nobalancechoice = input ('1. 충전하기\n2. 메인 메뉴로 돌아가기\n선택: ')
      if nobalancechoice == '1':
        self.charge_balance()
      elif nobalancechoice == '2':
        return
    
    print(f"\n이름: {self.user.name}")
    print(f"잔액: {self.user.balance}원")
    print(f"등록 계좌: {self.user.account if self.user.account else '없음'}")
    print(f"보유포인트: {self.user.points}p")

  # 2
  def charge_balance(self):
    if not self.user.account:
      print ('계좌가 존재하지 않습니다.')
      self.user.register_account()
    amount = self.prompt_integer("충전할 금액을 입력하세요: ")
    self.user.charge_balance(amount)

  # 3
  def transfer(self):
    if not self.user.account:
      print ('계좌가 존재하지 않아 송금이 불가합니다.')
      self.user.register_account()
    amount = self.prompt_integer("송금할 금액을 입력하세요: ")
    self.user.ensure_balance(amount)
    recipient_name = input("송금 받을 사람의 이름: ")
    recipient_bank = input("송금 받을 사람의 은행명: ")
    recipient_account = input("송금 받을 사람의 계좌번호: ")
    self.user.transfer(amount, recipient_name, recipient_bank,
                       recipient_account)

  # 4
  def pay(self):
    if not self.user.account:
      print ('계좌가 등록되지 않아 결제가 불가합니다.')
      self.user.register_account()
    amount = self.prompt_integer("결제할 금액을 입력하세요: ")
    self.user.ensure_balance(amount)
    recheck = input (f'결제하시겠습니까? 결제 금액은 {amount}, '
                     +f'적립은 {int(float(amount)*0.05)}원입니다. (y/n): ')
    if recheck.lower() == 'y':
      self.user.balance -= amount
      self.user.points += int(float(amount)*0.05)
      print ('결제가 완료되었습니다.')
      print (f'잔액은 {self.user.balance}원입니다.')
      print (f'적립 포인트: {self.user.points}p, 보유 포인트: {self.user.points}p')
      addpointyn = input ('추가 포인트를 적립하시겠습니까? (y/n): ')
      if addpointyn.lower() == 'y':
        addpoint = input ('임의의 숫자를 입력해주세요...')
        random_point = random.randint(1, 100)
        print(f'축하합니다! {addpoint} 선택 결과 {random_point}p가 추가되었습니다.')
        self.user.points += random_point
      elif addpointyn.lower() == 'n':
        print ('메인 메뉴로 돌아갑니다.')
    elif recheck.lower() == 'n':
      return
  
  # 5
  def register_gift_card(self):
    while True:
      try:
        card_number = input("기프트카드 번호를 입력하세요 (예: a-1234-5678-901): ")
        if card_number.lower == 'q':
          print('메인 메뉴로 돌아갑니다.')
          return
        elif self.validate_gift_card_number(card_number):
          prefix = card_number.split('-')[0].lower()
          amount_map = {'p': 50000, 'q': 30000, 'r': 10000}
          amount = amount_map.get(prefix, 5000)
          print(f"이 기프트카드로 {amount}원이 충전됩니다.")
          confirm = input("등록을 진행하시겠습니까? (y/n): ")
          if confirm.lower() == 'y':
            self.user.charge_balance(amount)
            print(f"기프트카드 등록 완료. 현재 잔액은 {self.user.balance}원입니다.")
            break
          else:
            print("기프트카드 등록이 취소되었습니다.")
            break
        else:
          print("잘못된 기프트카드 번호 형식입니다. 올바른 형식으로 입력해주세요.")
      except UnicodeDecodeError:
        print("입력 인코딩에 문제가 발생했습니다. 다시 입력해주세요.")

  def validate_gift_card_number(self, card_number):
    import re
    pattern = re.compile(r'^[a-zA-Z]-\d{4}-\d{4}-\d{3}$')
    return bool(pattern.match(card_number))


def main():
  print("프로그램을 시작합니다. 사용자의 이름을 입력하세요.")
  user_name = input("이름: ")
  user = User(user_name)
  menu = MenuManager(user)
  print (f'환영합니다, {user_name}님!')
  menu.main_menu()


if __name__ == "__main__":
  main()