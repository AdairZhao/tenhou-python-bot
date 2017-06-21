import unittest

from mahjong.hand_calculation.divider import HandDivider
from utils.tests import TestMixin


class YakuCalculationTestCase(unittest.TestCase, TestMixin):

    def setUp(self):
        self.divider = HandDivider()

    def cast_36_sets_to_strings(self, item):
        # cast 36 sets to 134 sets
        sets = [list(map(lambda y: y * 4, x)) for x in item]
        return [self._to_string(x) for x in sets]

    def test_hand_dividing_simple_case(self):
        tiles_34 = self._string_to_34_array(man='234567', sou='23455', honors='777')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 1)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['234m', '567m', '234s', '55s', '777z']
        )

    def test_hand_dividing_check_all_suits(self):
        tiles_34 = self._string_to_34_array(man='123', pin='123', sou='123', honors='11222')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 1)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['123m', '123p', '123s', '11z', '222z']
        )

    def test_hand_dividing_correct_pair(self):
        tiles_34 = self._string_to_34_array(man='23444', pin='344556', sou='333')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 1)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['234m', '44m', '345p', '456p', '333s']
        )

    def test_hand_dividing_hand_with_multiple_options(self):
        tiles_34 = self._string_to_34_array(man='11122233388899')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 2)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['123m', '123m', '123m', '888m', '99m']
        )
        self.assertEqual(
            self.cast_36_sets_to_strings(result[1]),
            ['111m', '222m', '333m', '888m', '99m']
        )

    def test_hand_dividing_second_hand_with_multiple_options(self):
        tiles_34 = self._string_to_34_array(man='112233', sou='445566', pin='99')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 2)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['123m', '123m', '99p', '456s', '456s']
        )
        self.assertEqual(
            self.cast_36_sets_to_strings(result[1]),
            ['11m', '22m', '33m', '99p', '44s', '55s', '66s']
        )

    def test_hand_dividing_one_suit_test_case(self):
        tiles_34 = self._string_to_34_array(sou='111123666789', honors='11')
        result = self.divider.divide_hand(tiles_34, [], [])
        self.assertEqual(len(result), 1)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['111s', '123s', '666s', '789s', '11z']
        )

    def test_hand_dividing_second_one_suit_test_case(self):
        tiles_34 = self._string_to_34_array(pin='234777888999', honors='22')
        open_sets = [self._string_to_open_34_set(pin='789'), self._string_to_open_34_set(pin='234')]
        result = self.divider.divide_hand(tiles_34, open_sets, [])
        self.assertEqual(len(result), 1)
        self.assertEqual(
            self.cast_36_sets_to_strings(result[0]),
            ['234p', '789p', '789p', '789p', '22z']
        )
