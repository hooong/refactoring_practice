import copy


def statement(invoice, plays):
    def enrich_performance(a_performance):
        result = copy.copy(a_performance)
        result['play'] = play_for(result)
        return result

    def play_for(a_performance):
        return plays[a_performance["playID"]]

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = list(map(enrich_performance, invoice['performances']))
    return render_plain_text(statement_data)


def render_plain_text(data):
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

    def total_volume_credits():
        result = 0
        for perf in data["performances"]:
            result += volume_credits_for(perf)
        return result

    def total_amount():
        result = 0
        for perf in data["performances"]:
            result += amount_for(perf)
        return result

    def usd(a_number):
        return f'{a_number/100:.2f}'

    result = f'청구 내역 (고객명: {data["customer"]})\n'

    for perf in data["performances"]:
        result += f' {perf["play"]["name"]}: ${usd(amount_for(perf))} ({perf["audience"]}석)\n'

    result += f'총액: ${usd(total_amount())}\n'
    result += f'적립 포인트: {total_volume_credits()}점'
    return result
