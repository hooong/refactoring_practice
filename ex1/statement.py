from ex1.create_statement_data import create_statement_data


def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


def render_plain_text(data):
    result = f'청구 내역 (고객명: {data["customer"]})\n'

    for perf in data["performances"]:
        result += f' {perf["play"]["name"]}: ${usd(perf["amount"])} ({perf["audience"]}석)\n'

    result += f'총액: ${usd(data["totalAmount"])}\n'
    result += f'적립 포인트: {data["totalVolumeCredits"]}점'
    return result


def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays))


def render_html(data):
    result = f'<h1>청구 내역 (고객명: {data["customer"]})</h1>\n'
    result += '<table>\n'
    result += '<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr>'
    for perf in data['performances']:
        result += f' <tr><td>{perf["play"]["name"]}</td><td>({perf["audience"]}석)</td>'
        result += f'<td>${usd(perf["amount"])}</td></tr>\n'
    result += '</table>\n'
    result += f'<p>총액: <em>${usd(data["totalAmount"])}</em>점</p>\n'
    result += f'<p>적립 포인트: <em>${usd(data["totalVolumeCredits"])}</em>점</p>\n'
    return result


def usd(a_number):
    return f'{a_number/100:.2f}'