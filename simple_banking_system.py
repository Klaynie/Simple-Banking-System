from enum import IntEnum

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
                 '\n'
                ,'\n'\
                 'Balance: 0'\
                 '\n']


def account_menu_handler():
    print(menu_prompts[MenuPrompt.ACCOUNT_MENU])
    result = None
    action = get_menu_choice()
    if action == AccountMenuChoice.EXIT:
        result = BaseMenuChoice.EXIT
    elif action == AccountMenuChoice.SHOW_BALANCE:
        print(user_messages[UserMessage.BALANCE])
    elif action == AccountMenuChoice.ACCOUNT_LOGOUT:
        print(user_messages[UserMessage.LOGOUT_OK])
        result = action
    return result


def account_loop(card_number, card_pin):
    stay_in_account_loop = True
    while stay_in_account_loop:
        result = account_menu_handler()
        if result == AccountMenuChoice.ACCOUNT_LOGOUT or result == BaseMenuChoice.EXIT:
            stay_in_account_loop = False
    return result


def is_valid_login(card_number, card_pin):
    return card_number == 4000004938320895 and card_pin == 6826


def login_to_account():
    result = None
    print(user_messages[UserMessage.CARD_PROMPT])
    card_number = int(input())
    print(user_messages[UserMessage.PIN_PROMPT])
    card_pin = int(input())
    if is_valid_login(card_number, card_pin):
        print(user_messages[UserMessage.LOGIN_OK])
        result = account_loop(card_number, card_pin)
    else:
        print(user_messages[UserMessage.WRONG_CARD_OR_PIN])
    return result


def create_account():
    print(user_messages[UserMessage.CARD_CREATION])
    card_number = 4000004938320895
    print(card_number)
    card_pin = 6826
    print(user_messages[UserMessage.PIN_CREATION])
    print(card_pin)
    print('\n')
    return card_number, card_pin
            

def get_menu_choice():
    return int(input())


def base_menu_handler():
    print(menu_prompts[MenuPrompt.BASE_MENU])
    result = None
    action = get_menu_choice()
    if action == BaseMenuChoice.EXIT:
        result = BaseMenuChoice.EXIT
    elif action == BaseMenuChoice.CREATE_ACCOUNT:
        create_account()
    elif action == BaseMenuChoice.ACCOUNT_LOGIN:
        result = login_to_account()
    return result


def banking_menu_loop():
    global menu_prompts, user_messages
    stay_in_banking_loop = True
    while stay_in_banking_loop:
        result = base_menu_handler()
        if result == BaseMenuChoice.EXIT:
            print(user_messages[UserMessage.EXIT])
            stay_in_banking_loop = False
        

if __name__ == "__main__":
    banking_menu_loop()