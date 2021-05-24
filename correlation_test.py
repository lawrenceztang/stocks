#!/usr/bin/env python3

import csv
import argparse
import os

STOCK_FILE_NAME = "historical_stock_prices.csv"

def make_stock_file(stocks, stock):
    file = open("stocks/" + stock, "w+")
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["ticker", "open", "close", "adj_close", "low", "high", "date"])
    for i in stocks:
        writer.writerow([i["ticker"], i["open"], i["close"], i["adj_close"], i["low"], i["high"], i["date"]])


def get_stocks(file_name, stock):
      if os.path.isfile("stock/" + stock):
          file_name = stock

      csvfile = open(file_name)

      reader = csv.DictReader(csvfile)
      stocks = []

      count = 0
      for i in reader:
          if(i["ticker"] == stock):
              stocks.append(i)
          count += 1

      if not os.path.isfile(stock):
          make_stock_file(stocks, stock)

      return stocks


def average_gain_after_positive(stocks):

    av_gain = 0
    count = 0

    for i in range(2, len(stocks)):
        if float(stocks[i - 1]["open"]) - float(stocks[i - 2]["open"]) > 0:
            av_gain += float(stocks[i]["open"]) - float(stocks[i - 1]["open"])
            count += 1

    return av_gain / count

def average_gain_after_turnaround(stocks):

    av_gain = 0
    count = 0

    for i in range(3, len(stocks)):
        if float(stocks[i - 1]["open"]) - float(stocks[i - 2]["open"]) > 0 and float(stocks[i - 2]["open"]) - float(stocks[i - 3]["open"]) < 0:
            av_gain += float(stocks[i]["open"]) - float(stocks[i - 1]["open"])
            count += 1

    return av_gain / count



def main(stock):
    stocks = get_stocks(STOCK_FILE_NAME, stock)
    print("Average gain after a positive delta: %f" % average_gain_after_positive(stocks))
    print("Average gain after a turnaround: %f" % average_gain_after_turnaround(stocks))
    print("Average gain in total: %f" % ((float(stocks[len(stocks) - 1]["open"]) - float(stocks[0]["open"])) / (len(stocks) - 1)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock", default="random")
    args = parser.parse_args()
    main(args.stock)
