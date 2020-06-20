import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
import sys


def load_price(ticker):
    df = pd.read_csv("./stock_dfs/" + ticker + ".csv")
    return df[['Date', 'Close']]


def price_change(p1, p2):
    return float(p2 / p1) - 1


def make_transaction(price, share, cash, totalshare):
    transaction = price * share
    if transaction > cash:
        return "Not enough balance"
    else:
        return transaction, cash - transaction, totalshare + share


def get_avg_cost(bookvalue, totalshares):
    return float(bookvalue / totalshares)


def get_upperbound(price, profit, avgcost):
    return price + profit / avgcost


def get_lowerbound(price, loss, avgcost):
    return price - loss / avgcost


def sell_all_stocks(price, totalshares):
    return price * totalshares


def draw_price_trend(date, closeprice):
    plt.plot(date, closeprice)
    plt.xticks(date[::60])
    plt.xticks(rotation=45)
    plt.show()


def print_tran_stats(accProfit, cashPosition, totalShares, costPerShare, currentPrice, upperBound, lowerBound):
    print("Accumulated profit: %f\n"
          "Cash position: %f\n"
          "Total shares: %d\n"
          "Cost per share: %f\n"
          "Current price: %f\nMarket "
          "value: %f\n"
          "upperBound: %f\n"
          "lowerBound: %f\n"
          % (accProfit, cashPosition, totalShares, costPerShare, currentPrice,
             currentPrice * totalShares, upperBound, lowerBound))


def main(target_ticker):
    """
    0. fix profit
    1. sell all at once
    2. sell when price reaches upper bound or lower bound
    3. sell when value drops below bearable loss
    4. buy more when it's up 3%
    """

    df = load_price(target_ticker)
    closePrice = list(df['Close'])
    date = list(df['Date'])

    budget = 2000
    cashPosition = budget
    targetProfit = 100
    bearableLoss = 90
    totalShares = 0
    sharePerTransaction = 10
    accProfit = 0
    buyMade = 0
    sellMade = 0
    totalBookValue = 0
    buyPrice = {}
    sellPrice = {}

    # buy at 1st day
    currentPrice = closePrice[0]

    transaction, cashPosition, totalShares = make_transaction(currentPrice, sharePerTransaction, cashPosition,
                                                              totalShares)
    totalBookValue += transaction
    costPerShare = get_avg_cost(totalBookValue, totalShares)
    upperBound = get_upperbound(currentPrice, targetProfit, costPerShare)
    lowerBound = get_lowerbound(currentPrice, bearableLoss, costPerShare)

    prevPrice = currentPrice

    for i in range(1, len(closePrice)):
        currentPrice = closePrice[i]

        # buy
        if price_change(prevPrice, currentPrice) >= 0.02:
            if cashPosition >= currentPrice * sharePerTransaction:
                transaction, cashPosition, totalShares = make_transaction(currentPrice, sharePerTransaction,
                                                                          cashPosition, totalShares)
                totalBookValue += transaction
                costPerShare = get_avg_cost(totalBookValue, totalShares)
                upperBound = get_upperbound(currentPrice, targetProfit, costPerShare)
                lowerBound = get_lowerbound(currentPrice, bearableLoss, costPerShare)

                # book keeping
                buyMade += 1
                buyPrice[date[i]] = currentPrice
                print(date[i])
                print_tran_stats(accProfit, cashPosition, totalShares, costPerShare, currentPrice, upperBound,
                                 lowerBound)

        # sell
        if (currentPrice >= upperBound or currentPrice <= lowerBound) and totalShares > 0:
            soldAmount = sell_all_stocks(currentPrice, totalShares)
            totalShares = 0
            cashPosition += soldAmount
            accProfit += soldAmount - totalBookValue
            totalBookValue = 0

            # book keeping
            sellMade += 1
            sellPrice[date[i]] = currentPrice
            print(date[i])
            print_tran_stats(accProfit, cashPosition, totalShares, costPerShare, currentPrice, upperBound, lowerBound)

            """
            reset profit target and usable cash position after selling
            """
            if budget < cashPosition:
                budget = cashPosition

            if currentPrice > targetProfit:
                targetProfit = currentPrice
                bearableLoss = 0.8 * targetProfit

        prevPrice = currentPrice

    print("Last trading date: " + date[-1])
    print("Final shares on hold: %d" % totalShares)
    print("Buy made: %d\nSell made: %d\n" % (buyMade, sellMade))

    # print("Bought at: ")
    # for k, v in buyPrice.items():
    #     print(k, v)
    #
    # print("\nSold at: ")
    # for k, v in sellPrice.items():
    #     print(k, v)

    # draw_price_trend(date, closePrice)


if __name__ == "__main__":
    # example: python strat.py AAPL
    ticker = sys.argv[1]
    main(ticker)
