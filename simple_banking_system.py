from enum import IntEnum
import sqlite3
import random

class BaseMenuChoice(IntEnum):
    EXIT = 0
    CREATE_ACCOUNT = 1
    ACCOUNT_LOGIN = 2

class AccountMenuChoice(IntEnum):
    EXIT = 0
    SHOW_BALANCE = 1
    ADD_INCOME = 2
    TRANSFER = 3
    CLOSE_ACCOUNT = 4
    ACCOUNT_LOGOUT = 5

class MenuPrompt(IntEnum):
    BASE_MENU = 0
    ACCOUNT_MENU = 1

class UserMessage(IntEnum):
    EXIT = 0
    CARD_CREATION = 1
    PIN_CREATION = 2
    CARD_PROMPT = 3
    PIN_PROMPT = 4
    LOGIN_OK = 5
    LOGOUT_OK = 6
    WRONG_CARD_OR_PIN = 7
    INCOME_PROMPT = 8
    INCOME_CONFIRM = 9
    CLOSE_ACCOUNT_CONFIRM = 10
    TRANSFER_CARD_PROMPT = 11
    NOT_PASSES_LUHN = 12
    CARD_NOT_EXIST = 13
    TRANSFER_AMOUNT_PROMPT = 14
    NOT_ENOUGH_MONEY = 15
    TRANSFER_OK = 16

class CreditCard(object):
    """ Represents a credit card.
    attributes: issuer_number, customer_account_number, check_digit, pin, balance
    """
    
    def __init__(self):
        self.issuer_number = '400000'
        self.customer_account_number = create_random_number_string(9)
        self.check_digit = '0'
        self.pin = create_random_number_string(4)
        self.balance = 0
    
    def calculate_control_number(self):
        number_string = self.issuer_number + self.customer_account_number
        number_list = [int(digit) for digit in number_string]
        for i, digit in enumerate(number_list, 0):
            if (i + 1) % 2 != 0:
                number_list[i] = number_list[i] * 2
                if number_list[i] > 9:
                    number_list[i] = number_list[i] - 9
        return sum(number_list)
    
    def set_check_digit(self):
        result = str((10 - self.calculate_control_number() % 10) % 10)
        self.check_digit = result
    
    def __str__(self):
        return self.issuer_number + self.customer_account_number + self.check_digit
    
    def get_card_number(self):
        return self.issuer_number + self.customer_account_number + self.check_digit
    
    def get_pin(self):
        return self.pin
    
    def get_balance(self):
        return self.balance
    
    def open_session(self):
        self.session_open = True
    
    def close_session(self):
        self.session_open = False


menu_prompts = ['1. Create an account\n'\
                '2. Log into account\n'\
                '0. Exit'
               ,'1. Balance\n'\
                '2. Add income\n'\
                '3. Do transfer\n'\
                '4. Close account\n'\
                '5. Log out\n'\
                '0. Exit']

user_messages = ['\n'\
                 'Bye!'
                ,'\n'\
                 'Your card has been created\n'\
                 'Your card number:'
                ,'Your card PIN:'
                ,'\n'\
                 'Enter your card number:'
                ,'Enter your PIN:'
                ,'\n'\
                 'You have successfully logged in!'\
                 '\n'
                ,'\n'\
                 'You have successfully logged out!'\
                 '\n'
                ,'\n'\
                 'Wrong card number or PIN!'\
                 '\n'
                ,'\n'\
                 'Enter income:'
                ,'Income was added!'\
                 '\n'
                ,'\n'\
                 'The account has been closed!'\
                 '\n'
                ,'\n'\
                 'Transfer\n'
                 'Enter card number:\n'
                ,'Probably you made mistake in the card number. Please try again!'\
                 '\n'
                ,'Such a card does not exist.'\
                 '\n'
                ,'Enter how much money you want to transfer:'
                ,'Not enough money!'\
                 '\n'
                ,'Success!'\
                 '\n']

def create_random_number_string(digits):
    return str(random.randrange(1, 10**digits)).zfill(digits)


def add_income_to_account(session, input_card_number, income):
    update_details = (income, input_card_number)
    c = session.cursor()
    c.execute('''UPDATE
                   card
                    SET
                balance = balance + ?
                  WHERE
                number = ?'''\
               ,update_details)
    session.commit()


def print_credit_card_balance(session, input_card_number):
    c = session.cursor()
    row = c.execute('''SELECT balance
                             FROM card
                        WHERE
                        number = ?'''\
                        ,(input_card_number,))
    balance = row.fetchone()[0]
    print(f'\nBalance: {balance}\n')


def close_account(session, input_card_number):
    c = session.cursor()
    row = c.execute('''DELETE FROM
                       card
                        WHERE
                       number = ?'''\
                     ,(input_card_number,))
    session.commit()
    print(user_messages[UserMessage.CLOSE_ACCOUNT_CONFIRM])


def is_valid_target_account(session, input_card_number, target_account):
    result = True
    if not passes_luhn_alogrithm(target_account):
        result = False
        print(user_messages[UserMessage.NOT_PASSES_LUHN])
    elif not already_exists(session, target_account):
        result = False
        print(user_messages[UserMessage.CARD_NOT_EXIST])
    return result


def is_valid_transfer_amount(session, card_number, transfer_amount):
    c = session.cursor()
    transfer_details = (card_number, transfer_amount)
    c.execute('''SELECT *
                   FROM card
                  WHERE
                number = ?
                AND
                balance >= ?'''\
               ,transfer_details)
    result = c.fetchone() is not None
    if result == False:
        print(user_messages[UserMessage.NOT_ENOUGH_MONEY])
    return result

def transfer_money(session, input_card_number):
    target_account = input(user_messages[UserMessage.TRANSFER_CARD_PROMPT])
    if is_valid_target_account(session, input_card_number, target_account):
        transfer_amount = request_integer(user_messages[UserMessage.TRANSFER_AMOUNT_PROMPT])
        if is_valid_transfer_amount(session, input_card_number, transfer_amount):
            add_income_to_account(session, input_card_number, -transfer_amount)
            add_income_to_account(session, target_account, transfer_amount)
            print(user_messages[UserMessage.TRANSFER_OK])


def account_menu_handler(session, input_card_number):
    result = None
    action = request_integer(menu_prompts[MenuPrompt.ACCOUNT_MENU])
    if action == AccountMenuChoice.EXIT:
        result = BaseMenuChoice.EXIT
    elif action == AccountMenuChoice.SHOW_BALANCE:
        print_credit_card_balance(session, input_card_number)
    elif action == AccountMenuChoice.ADD_INCOME:
        income = request_integer(user_messages[UserMessage.INCOME_PROMPT])
        add_income_to_account(session, input_card_number, income)
        print(user_messages[UserMessage.INCOME_CONFIRM])
    elif action == AccountMenuChoice.TRANSFER:
        transfer_money(session, input_card_number)
    elif action == AccountMenuChoice.CLOSE_ACCOUNT:
        close_account(session, input_card_number)
        result = AccountMenuChoice.ACCOUNT_LOGOUT
    elif action == AccountMenuChoice.ACCOUNT_LOGOUT:
        result = AccountMenuChoice.ACCOUNT_LOGOUT
        print(user_messages[UserMessage.LOGOUT_OK])
    return result


def account_loop(session, card_number):
    keep_in_account_menu = True
    while keep_in_account_menu:
        result = account_menu_handler(session, card_number)
        if result == BaseMenuChoice.EXIT\
        or result == AccountMenuChoice.ACCOUNT_LOGOUT:
            keep_in_account_menu = False
    return result


def is_valid_login(session, card_number, card_pin):
    c = session.cursor()
    account_details = (card_number, card_pin)
    c.execute('''SELECT *
                   FROM card
                  WHERE
                number = ?
                AND
                pin = ?'''\
               ,account_details)
    result = c.fetchone() is not None
    return result


def passes_luhn_alogrithm(number_string):
    number_list = [int(digit) for digit in number_string]
    for j, digit in enumerate(number_list, 0):
        if (j + 1) % 2 != 0:
            number_list[j] = number_list[j] * 2
            if number_list[j] > 9:
                number_list[j] = number_list[j] - 9
    result = sum(number_list) % 10 == 0
    return result


def get_login_information():
    print(user_messages[UserMessage.CARD_PROMPT])
    input_card_number = input()
    print(user_messages[UserMessage.PIN_PROMPT])
    input_card_pin = input()
    return input_card_number, input_card_pin


def login_to_account(session):
    result = None
    card_number, card_pin = get_login_information()
    if is_valid_login(session, card_number, card_pin):
        print(user_messages[UserMessage.LOGIN_OK])
        result = account_loop(session, card_number)
    else:
        print(user_messages[UserMessage.WRONG_CARD_OR_PIN])
    return result


def create_credit_card():
    result = CreditCard()
    result.set_check_digit()
    return result


def print_credit_card_info(credit_card):
    print(user_messages[UserMessage.CARD_CREATION])
    print(credit_card)
    print(user_messages[UserMessage.PIN_CREATION])
    print(credit_card.pin)
    print('\n')


def create_account(session):
    keep_in_account_creation = True
    while keep_in_account_creation:
        credit_card = create_credit_card()
        card_number = credit_card.get_card_number()
        if not already_exists(session, card_number):
            keep_in_account_creation = False
            save_account(session, credit_card)
            print_credit_card_info(credit_card)


def already_exists(session, card_number):
    c = session.cursor()
    card_number = (card_number,)
    c.execute('''SELECT *
                   FROM card
                  WHERE
                number = ?'''\
               ,card_number)
    result = c.fetchone() is not None
    return result


def save_account(session, credit_card):
    c = session.cursor()
    card_number = credit_card.get_card_number()
    card_pin = credit_card.get_pin()
    account_info = (card_number, card_pin)
    c.execute('''INSERT INTO
                   card (
                 number,
                 pin
                )
                 VALUES (
                 ?,
                 ?
                )'''\
               ,account_info)
    session.commit()
            

def request_integer(message):
    print(message)
    return int(input())


def base_menu_handler(session):
    action = request_integer(menu_prompts[MenuPrompt.BASE_MENU])
    if action == BaseMenuChoice.EXIT:
        result = BaseMenuChoice.EXIT
    elif action == BaseMenuChoice.CREATE_ACCOUNT:
        result = create_account(session)
    elif action == BaseMenuChoice.ACCOUNT_LOGIN:
        result = login_to_account(session)
    return result


def banking_menu_loop(session):
    global menu_prompts, user_messages
    stay_in_banking_loop = True
    while stay_in_banking_loop:
        result = base_menu_handler(session)
        if result == BaseMenuChoice.EXIT:
            print(user_messages[UserMessage.EXIT])
            stay_in_banking_loop = False

def setup_database():
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS card (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 number TEXT,
                 pin TEXT,
                 balance INTEGER DEFAULT 0)''')


if __name__ == "__main__":
    setup_database()
    new_session = sqlite3.connect('card.s3db')
    banking_menu_loop(new_session)