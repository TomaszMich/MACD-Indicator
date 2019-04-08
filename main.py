import pandas as pd


def EMA(currentDay, period, samples):
    nominator = samples[currentDay]
    denominator = 1
    oneMinusAlpha = 1 - (2 / (period + 1))

    for i in range(1, period + 1):
        if currentDay - i < 0:
            continue
        tmp = pow(oneMinusAlpha, i)
        nominator += tmp * samples[currentDay - i]
        denominator += tmp

    return nominator / denominator


def MACD(currentDay, samples):
    return EMA(currentDay, 12, samples) - EMA(currentDay, 26, samples)


if __name__ == "__main__":
    data = pd.read_csv("wig20.csv")
    samples = data['Zamkniecie']
    macd = []
    signal = []
    wallet = []
    diff = 0.0  # variable to store difference between MACD and SIGNAL
    N = 1000
    stock = 1000
    cash = 0
    q = 300     # quantity of stock to buy/sell

    for j in range(0, N):
        macd.append(MACD(j, samples))
        signal.append(EMA(j, 9, macd))

    i = 0
    while i < N:
        wallet.append((stock * samples[i]) + cash)
        if i < 27:  # begin transactions after first 26 days
            i += 1
            continue
        diff = macd[i] - signal[i]
        if abs(diff) < 0.6 and abs(macd[i]) >= 30:  # close to each other and big change
            if diff < 0 and cash >= q * samples[i]:     # SIGNAL above MACD -> buy
                cash -= q * samples[i]
                stock += q
            elif diff > 0 and stock >= q:  # MACD above SIGNAL -> sell
                cash += q * samples[i]
                stock -= q
            for j in range(0, 9):   # skipping few days
                wallet.append((stock * samples[i]) + cash)
                i += 1
        i += 1

    final = wallet[N - 1]
    profit = final - wallet[0]
    zysk = profit/wallet[0] * 100

    print("Początkowo:", wallet[0], "\nGotówka:", cash, "\nAkcje:", stock, "\nProfit:", profit, "\nZysk:", zysk, "%")





