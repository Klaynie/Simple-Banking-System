from unittest import mock
from unittest.mock import patch, call
from unittest import TestCase
from simple_banking_system import *

class AlreadyExistsCardNumberCases(TestCase):
    def test_already_exists_card_01(self):
        session = sqlite3.connect('card.s3db')
        credit_card = CreditCard()
        credit_card.issuer_number = '400000'
        credit_card.customer_account_number = '003669456'                                               
        credit_card.check_digit = '2'
        self.assertTrue(already_exists(session, credit_card))
    def test_already_exists_card_02(self):
        session = sqlite3.connect('card.s3db')
        credit_card = CreditCard()
        credit_card.issuer_number = '300000'
        credit_card.customer_account_number = '742416163'                                               
        credit_card.check_digit = '3'
        self.assertFalse(already_exists(session, credit_card))

class IsValidLoginCases(TestCase):
    def test_correct_login(self):
        session = sqlite3.connect('card.s3db')
        card_number = '4000000036694562'
        card_pin = '0854'
        self.assertTrue(is_valid_login(session, card_number, card_pin))
    def test_incorrect_login(self):
        session = sqlite3.connect('card.s3db')
        card_number = '4000007424161633'
        card_pin = '1337'
        self.assertFalse(is_valid_login(session, card_number, card_pin))

class CalculateControlNumberCases(TestCase):
    def test_control_number_calculation_01(self):
        credit_card = CreditCard()
        credit_card.customer_account_number = '844943340'
        control_number = 57
        self.assertEqual(credit_card.calculate_control_number(), control_number)
    
class TestLuhnAlogrithmCases(TestCase):
    def test_luhn_alogrithm_01(self):
        result = 0
        for i in range(100000):
            credit_card = CreditCard()
            credit_card.set_check_digit()
            number_string = credit_card.get_card_number()
            number_list = [int(digit) for digit in number_string]
            for j, digit in enumerate(number_list, 0):
                if (j + 1) % 2 != 0:
                    number_list[j] = number_list[j] * 2
                    if number_list[j] > 9:
                        number_list[j] = number_list[j] - 9
            result += sum(number_list) % 10
        self.assertTrue(result == 0)
    def test_luhn_alogrithm_02(self):
        number_string = '4000007424161633'
        self.assertTrue(passes_luhn_alogrithm(number_string))
    def test_luhn_alogrithm_03(self):
        number_string = '4000007424161623'
        self.assertFalse(passes_luhn_alogrithm(number_string))