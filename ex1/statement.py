from ex1.create_statement_data import create_statement_data


def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


def render_plain_text(data):
    def usd(a_number):
        return f'{a_number/100:.2f}'

    result = f'청구 내역 (고객명: {data["customer"]})\n'

    for perf in data["performances"]:
        result += f' {perf["play"]["name"]}: ${usd(perf["amount"])} ({perf["audience"]}석)\n'

    result += f'총액: ${usd(data["totalAmount"])}\n'
    result += f'적립 포인트: {data["totalVolumeCredits"]}점'
    return result
