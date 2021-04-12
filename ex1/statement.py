import copy
from functools import reduce


def statement(invoice, plays):
    def enrich_performance(a_performance):
        result = copy.copy(a_performance)
        result['play'] = play_for(result)
        result['amount'] = amount_for(result)
        result['volumeCredits'] = volume_credits_for(result)
        return result

    def play_for(a_performance):
        return plays[a_performance["playID"]]

    def amount_for(a_performance):
        if a_performance['play']['type'] == 'tragedy':
            result = 40000
            if a_performance["audience"] > 30:
                result += 1000 * (a_performance["audience"] - 30)
        elif a_performance['play']['type'] == 'comedy':
            result = 30000
            if a_performance["audience"] > 20:
                result += 10000 + 500 * (a_performance["audience"] - 20)
            result += 300 * a_performance["audience"]
        else:
            raise Exception(f'알 수 없는 장르 : {a_performance["play"]["type"]}')
        return result

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
    return render_plain_text(statement_data)


def render_plain_text(data):
    def usd(a_number):
        return f'{a_number/100:.2f}'

    result = f'청구 내역 (고객명: {data["customer"]})\n'

    for perf in data["performances"]:
        result += f' {perf["play"]["name"]}: ${usd(perf["amount"])} ({perf["audience"]}석)\n'

    result += f'총액: ${usd(data["totalAmount"])}\n'
    result += f'적립 포인트: {data["totalVolumeCredits"]}점'
    return result
