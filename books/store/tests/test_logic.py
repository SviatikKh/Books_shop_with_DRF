from django.test import TestCase

from store.logic import operations


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 10, '+')
        self.assertEqual(16, result)

    def test_minus(self):
        result = operations(10, 5, '-')
        self.assertEqual(5, result)

    def test_mгд(self):
        result = operations(10, 5, '*')
        self.assertEqual(50, result)
