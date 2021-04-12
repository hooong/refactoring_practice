import json
import unittest

from ex1.statement import statement, html_statement


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
            result += statement(invoice, self.plays)

        expected = '청구 내역 (고객명: BicCo)\n' \
                   ' Hamlet: $650.00 (55석)\n' \
                   ' As You Like It: $580.00 (35석)\n' \
                   ' Othello: $500.00 (40석)\n' \
                   '총액: $1730.00\n' \
                   '적립 포인트: 47점'
        self.assertEqual(expected, result)

    def test_valid_statement_html(self):
        result = ''

        for invoice in self.invoices:
            result += html_statement(invoice, self.plays)

        expected = '<h1>청구 내역 (고객명: BicCo)</h1>\n' \
                   '<table>\n' \
                   '<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr>' \
                   ' <tr><td>Hamlet</td><td>(55석)</td><td>$650.00</td></tr>\n' \
                   ' <tr><td>As You Like It</td><td>(35석)</td><td>$580.00</td></tr>\n' \
                   ' <tr><td>Othello</td><td>(40석)</td><td>$500.00</td></tr>\n</table>\n' \
                   '<p>총액: <em>$1730.00</em>점</p>\n' \
                   '<p>적립 포인트: <em>$0.47</em>점</p>\n'
        self.assertEqual(expected, result)