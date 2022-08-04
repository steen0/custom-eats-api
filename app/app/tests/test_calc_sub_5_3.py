from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.subtract(5, 3)
        
        self.assertEqual(res,2)
