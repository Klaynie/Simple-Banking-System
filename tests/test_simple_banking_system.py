from unittest import mock
from unittest.mock import patch, call
from unittest import TestCase
from simple_banking_system import *

class IsValidCardNumberCases(TestCase):
    def test_valid_card_01(self):
        credit_card = CreditCard()
        credit_card.customer_account_number = '844943340'
        credit_card.check_digit = '3'
        input_card_number = '4000008449433403'
        self.assertTrue(is_valid_card_number(credit_card, input_card_number))

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