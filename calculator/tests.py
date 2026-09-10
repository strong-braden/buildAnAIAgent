# calculator/tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_addition(self) -> None:
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self) -> None:
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self) -> None:
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self) -> None:
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self) -> None:
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self) -> None:
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_modulo(self) -> None:
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_exponentiation(self) -> None:
        result = self.calculator.evaluate("2 ** 3")
        self.assertEqual(result, 8)

    def test_exponentiation_precedence(self) -> None:
        result = self.calculator.evaluate("2 ** 3 ** 2")  # Should be 2^(3^2) = 2^9 = 512
        self.assertEqual(result, 512)

    def test_unary_negative(self) -> None:
        result = self.calculator.evaluate("-5 + 3")
        self.assertEqual(result, -2)

    def test_unary_positive(self) -> None:
        result = self.calculator.evaluate("+5 * 2")
        self.assertEqual(result, 10)

    def test_parentheses(self) -> None:
        result = self.calculator.evaluate("(3 + 5) * 2")
        self.assertEqual(result, 16)

    def test_nested_parentheses(self) -> None:
        result = self.calculator.evaluate("(2 + 3) * (4 - 1)")
        self.assertEqual(result, 15)

    def test_complex_precedence(self) -> None:
        result = self.calculator.evaluate("3 + 4 * 2 ** 2 - (1 + 3)")
        self.assertEqual(result, 14)

    def test_empty_expression(self) -> None:
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_whitespace_only(self) -> None:
        result = self.calculator.evaluate("   ")
        self.assertIsNone(result)

    def test_invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_division_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("10 / 0")

    def test_invalid_number(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 + 2.5.3")

    def test_mismatched_parentheses(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("(3 + 5")

    def test_unexpected_closing_paren(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 + )")

    def test_operator_where_number_expected(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 + * 4")

    def test_number_where_operator_expected(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3 4 + 5")

    def test_multiple_decimals_in_number(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("3.2.5")

    def test_complex_float_expression(self) -> None:
        result = self.calculator.evaluate("3.5 * 2.1")
        self.assertAlmostEqual(result, 7.35, places=5)

    def test_result_integer_conversion(self) -> None:
        # Even though evaluate returns float, we should test that
        # floats that are whole numbers will be properly handled elsewhere
        result = self.calculator.evaluate("4 / 2")
        self.assertEqual(result, 2.0)

    def test_negative_division_result(self) -> None:
        result = self.calculator.evaluate("10 / -3")
        self.assertAlmostEqual(result, -10 / 3, places=10)


if __name__ == "__main__":
    unittest.main()