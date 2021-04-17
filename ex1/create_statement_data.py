import copy
from functools import reduce


class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self._performance = a_performance
        self._play = a_play
        self._amount = self.calc_amount()
        self.volume_credits = self.volume_credits()

    def calc_amount(self):
        raise Exception('서브클래스에서 처리하도록 설계 됨.')

    def volume_credits(self):
        return max(self._performance["audience"] - 30, 0)

    @property
    def performance(self):
        return self._performance

    @property
    def play(self):
        return self._play

    @property
    def amount(self):
        return self._amount


class TragedyCalculator(PerformanceCalculator):
    def calc_amount(self):
        result = 40000
        if self.performance["audience"] > 30:
            result += 1000 * (self.performance["audience"] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    def calc_amount(self):
        result = 30000
        if self.performance["audience"] > 20:
            result += 10000 + 500 * (self.performance["audience"] - 20)
        result += 300 * self.performance["audience"]
        return result

    def volume_credits(self):
        return super().volume_credits() + self.performance["audience"] // 5


def create_performance_calculator(a_performance, a_play):
    if a_play['type'] == 'tragedy':
        return TragedyCalculator(a_performance, a_play)
    elif a_play['type'] == 'comedy':
        return ComedyCalculator(a_performance, a_play)
    else:
        raise Exception(f'알 수 없는 장르 : {a_play["type"]}')        


def create_statement_data(invoice, plays):
    def enrich_performance(a_performance):
        calculator = create_performance_calculator(a_performance, play_for(a_performance))
        result = copy.copy(a_performance)
        result['play'] = calculator.play
        result['amount'] = calculator.amount
        result['volumeCredits'] = calculator.volume_credits
        return result

    def play_for(a_performance):
        return plays[a_performance["playID"]]

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