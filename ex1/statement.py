def statement(invoice, plays):
    def amount_for(a_performance, play):
        if play['type'] == 'tragedy':
            result = 40000
            if a_performance["audience"] > 30:
                result += 1000 * (a_performance["audience"] - 30)
        elif play['type'] == 'comedy':
            result = 30000
            if a_performance["audience"] > 20:
                result += 10000 + 500 * (a_performance["audience"] - 20)
            result += 300 * a_performance["audience"]
        else:
            raise Exception(f'알 수 없는 장르 : {play["type"]}')
        return result

    def play_for(a_performance):
        return plays[a_performance["playID"]]

    total_amount = 0
    volume_credits = 0
    result = f'청구 내역 (고객명: {invoice["customer"]})\n'

    for perf in invoice["performances"]:
        this_amount = 0

        this_amount = amount_for(perf, play_for(perf))

        # 포인트 적립
        volume_credits += max(perf["audience"] - 30, 0)
        # 희극 관객 5명당 추가 포인트 제공
        if 'comedy' == play_for(perf)['type']:
            volume_credits += perf["audience"] // 5

        # 청구 내역 출력
        result += f' {play_for(perf)["name"]}: ${(this_amount/100):.2f} ({perf["audience"]}석)\n'
        total_amount += this_amount

    result += f'총액: ${(total_amount/100):.2f}\n'
    result += f'적립 포인트: {volume_credits}점'
    return result



