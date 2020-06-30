from enum import IntEnum
import random

class BaseMenuChoice(IntEnum):
    EXIT = 0
    CREATE_ACCOUNT = 1
    ACCOUNT_LOGIN = 2

class AccountMenuChoice(IntEnum):
    EXIT = 0
    SHOW_BALANCE = 1
    ACCOUNT_LOGOUT = 2

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
    BALANCE = 8

class CreditCard(object):
    """ Represents a credit card.
    attributes: issuer_number, customer_account_number, check_digit, pin, balance
    """
    
    def __init__(self):
        self.issuer_number = '400000'
        self.customer_account_number = create_random_n_digit_number_string(9)
        self.check_digit = str(random.randrange(0, 9))
        self.pin = create_random_n_digit_number_string(4)
        self.balance = 0
        self.session_open = False
    
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
                 '2. Log out\n'\
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
                 '\n']

def create_random_n_digit_number_string(number_of_digits):
    return str(random.randrange(1, 10**number_of_digits)).zfill(number_of_digits)

def print_credit_card_balance(credit_card):
    balance = credit_card.get_balance()
    print(f'\nBalance: {balance}\n')

def account_menu_handler(credit_card):
    print(menu_prompts[MenuPrompt.ACCOUNT_MENU])
    result = credit_card
    action = get_menu_choice()
    if action == AccountMenuChoice.EXIT:
        credit_card.close_session()
        result = BaseMenuChoice.EXIT
    elif action == AccountMenuChoice.SHOW_BALANCE:
        print_credit_card_balance(credit_card)
    elif action == AccountMenuChoice.ACCOUNT_LOGOUT:
        credit_card.close_session()
        print(user_messages[UserMessage.LOGOUT_OK])
    return result


def account_loop(credit_card):
    credit_card.open_session()
    while credit_card.session_open:
        result = account_menu_handler(credit_card)
    return result


def is_valid_login(credit_card, input_card_number, input_card_pin):
    is_valid_card = input_card_number == credit_card.get_card_number()
    is_correct_pin = input_card_pin == credit_card.get_pin()
    return is_valid_card and is_correct_pin


def login_to_account(credit_card):
    result = credit_card
    print(user_messages[UserMessage.CARD_PROMPT])
    input_card_number = input()
    print(user_messages[UserMessage.PIN_PROMPT])
    input_card_pin = input()
    if is_valid_login(credit_card, input_card_number, input_card_pin):
        print(user_messages[UserMessage.LOGIN_OK])
        result = account_loop(credit_card)
    else:
        print(user_messages[UserMessage.WRONG_CARD_OR_PIN])
    return result


def create_account():
    result = CreditCard()
    print(user_messages[UserMessage.CARD_CREATION])
    print(result)
    print(user_messages[UserMessage.PIN_CREATION])
    print(result.pin)
    print('\n')
    return result
            

def get_menu_choice():
    return int(input())


def base_menu_handler(credit_card=None):
    print(menu_prompts[MenuPrompt.BASE_MENU])
    action = get_menu_choice()
    if action == BaseMenuChoice.EXIT:
        result = BaseMenuChoice.EXIT
    elif action == BaseMenuChoice.CREATE_ACCOUNT:
        result = create_account()
    elif action == BaseMenuChoice.ACCOUNT_LOGIN:
        result = login_to_account(credit_card)
    return result


def banking_menu_loop():
    global menu_prompts, user_messages
    stay_in_banking_loop = True
    result = None
    while stay_in_banking_loop:
        result = base_menu_handler(result)
        if result == BaseMenuChoice.EXIT:
            print(user_messages[UserMessage.EXIT])
            stay_in_banking_loop = False
        

if __name__ == "__main__":
    banking_menu_loop()