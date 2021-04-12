import json
import unittest

from ex1.statement import statement


class StatementTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('invoices.json', 'r') as f:
            cls.invoices = json.load(f)

        with open('plays.json', 'r') as f:
            cls.plays = json.load(f)

    def test_valid_statement(self):
        result = ''

        for invoice in self.invoices:
            result = statement(invoice, self.plays)

        expected = '청구 내역 (고객명: BicCo)\n Hamlet: $650.00 (55석)\n As You Like It: $580.00 (35석)\n Othello: $500.00 (40석)\n총액: $1730.00\n적립 포인트: 47점'
        self.assertEqual(expected, result)
