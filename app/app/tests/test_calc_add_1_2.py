from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    def test_subtract_numbers(self):
        res = calc.add(1, 2)
        
        self.assertEqual(res, 3)
