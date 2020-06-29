from unittest import mock
from unittest.mock import patch, call
from unittest import TestCase
from simple_banking_system import *

class IsValidCardCases(TestCase):
    def test_valid_card_01(self):
        card_number = 4000004938320895
        card_pin = 6826
        self.assertTrue(is_valid_login(card_number, card_pin))