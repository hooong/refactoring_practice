import copy
from functools import reduce


class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play
        self.amount = self.amount()

    def amount(self):
        if self.play["type"] == 'tragedy':
            result = 40000
            if self.performance["audience"] > 30:
                result += 1000 * (self.performance["audience"] - 30)
        elif self.play['type'] == 'comedy':
            result = 30000
            if self.performance["audience"] > 20:
                result += 10000 + 500 * (self.performance["audience"] - 20)
            result += 300 * self.performance["audience"]
        else:
            raise Exception(f'알 수 없는 장르 : {self.play["type"]}')
        return result


def create_statement_data(invoice, plays):
    def enrich_performance(a_performance):
        calculator = PerformanceCalculator(a_performance, play_for(a_performance))
        result = copy.copy(a_performance)
        result['play'] = calculator.play
        result['amount'] = calculator.amount
        result['volumeCredits'] = volume_credits_for(result)
        return result

    def play_for(a_performance):
        return plays[a_performance["playID"]]

    def amount_for(a_performance):
        return PerformanceCalculator(a_performance, play_for(a_performance)).amount

    def volume_credits_for(a_performance):
        result = 0
        result += max(a_performance["audience"] - 30, 0)
        if 'comedy' == a_performance['play']['type']:
            result += a_performance["audience"] // 5
        return result

    def total_volume_credits(data):
        return reduce(lambda total, p: total + p['volumeCredits'], data['performances'], 0)

    def total_amount(data):
        return reduce(lambda total, p: total + p['amount'], data['performances'], 0)

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = list(map(enrich_performance, invoice['performances']))
    statement_data['totalAmount'] = total_amount(statement_data)
    statement_data['totalVolumeCredits'] = total_volume_credits(statement_data)
    return statement_data