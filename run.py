#!/usr/bin/env python3

import csv
import sys
import matplotlib.pyplot as plt
import threading
import time
import os.path
import random
from bst import Node, search, insert, inorder
import argparse

ACTION_BUY = 1
ACTION_SELL = 2
ACTION_STOP = 3
OUTPUT_NAME = "stocks_list.txt"
DAYS_AFTER_INITIAL = 60

current_price = 0
start_price = 0

def str_to_year(str):
    try:
        return int(str)
    except:
        return -1

def str_year_greater_eq_than(str, year):
    return int(str.split("-")[0]) >= year

def plot(x, y, stock):
        plt.clf()
        _ = plt.plot(x, y)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Price of " + stock + " over time")
        plt.draw()

def str_to_act(str):
    if str == "b":
        return ACTION_BUY
    if str == "s":
        return ACTION_SELL
    if str == "x":
        return ACTION_STOP

class StockSim:

    def random_stock(self):
        if not os.path.isfile(self.output_name):
            self.make_stocks_list()

        f = open(self.output_name)
        num = int(f.readline())
        rand = random.randint(0, num)
        i = 0
        for line in f:
            if i == rand:
                return line[:-1]
            i += 1

    def make_stocks_list(self):
        csvfile = open(self.file_name   )
        reader = csv.DictReader(csvfile)

        tree = Node(reader.__next__()["ticker"])

        count = 0
        for i in reader:
            if(not search(tree, i["ticker"])):
                insert(tree, i["ticker"])
                count += 1

        list = inorder(tree)
        f = open(self.output_name, "a")
        f.write(str(count + 1) + "\n")
        for i in inorder(tree):
            f.write(i + "\n")

    def get_stocks(self):
        csvfile = open(self.file_name)

        reader = csv.DictReader(csvfile)
        self.stocks = []

        count = 0
        for i in reader:
            if(count >= DAYS_AFTER_INITIAL and i["ticker"] == self.stock and str_year_greater_eq_than(i["date"], self.year)):
                self.stocks.append(i)
            count += 1

    def get_buy_delta(self):
        min_buy = float(self.stocks[self.current_index]["open"])
        for i in range(max(self.current_index - self.average_sell_interval, 0),
                       min(self.current_index + self.average_sell_interval, len(self.stocks))):

            min_buy = min(float(self.stocks[i]["open"]), min_buy)
        delta = (float(self.stocks[self.current_index]["open"]) - min_buy) / min_buy
        return delta

    def get_sell_delta(self):
        max_sell = float(self.stocks[self.current_index]["open"])
        for i in range(max(self.current_index - self.average_sell_interval, 0),
                       min(self.current_index + self.average_sell_interval, len(self.stocks))):

            max_sell = max(float(self.stocks[i]["open"]), max_sell)
        delta = (float(self.stocks[self.current_index]["open"]) - max_sell) / max_sell
        return delta

    def get_relative_buy_rating(self):
        rating = self.get_buy_delta()
        self.buy_rating_sum += rating
        self.buy_num += 1
        return self.buy_rating_sum / self.buy_num - rating

    def get_relative_sell_rating(self):
        rating = self.get_sell_delta()
        self.sell_rating_sum += rating
        self.sell_num += 1
        return self.sell_rating_sum / self.sell_num - rating

    def print_data(self):
        percent_change = ((float(self.stocks[self.current_index]["open"]) - self.start_price) / self.start_price * 100)
        print("Stock change over time: %f%%" % percent_change)
        print("Stock change for time held: %f%%" % (percent_change * self.time_held / self.current_index))
        print("Money made: %f%%" % (self.money_made / self.start_price * 100))

    def buy_sell_thread(self):

        print("Enter action (b for buy, s for sell, x to quit)")

        i = 0
        while True:
            action = str_to_act(input(""))
            current_price = float(self.stocks[self.current_index]["open"])
            if action == ACTION_BUY:
                if self.bought_index == -1:
                    self.bought_index = self.current_index
                    print("Bought stock for %f" % current_price)
                    if self.get_relative_buy_rating() > 0:
                        print("Good buy!!!!")
                    else:
                        print("You suck - bad buy")
                else:
                    print("Already have stock - can't buy")
            elif action == ACTION_SELL:
                if self.bought_index != -1:
                    self.money_made += current_price - float(self.stocks[self.bought_index]["open"])
                    self.time_held += self.current_index - self.bought_index
                    self.bought_index = -1
                    print("Sold stock for %f" % current_price)
                    print("Money made: %f" % self.money_made)
                    if self.get_relative_sell_rating() > 0:
                        print("Good sell!!!!")
                    else:
                        print("You suck - bad sell")
                else:
                    print("Don't have stock - can't sell")
            elif action == ACTION_STOP:
                self.print_data()
                exit()
            if i % 10 == 1:
                self.print_data()
            i += 1

    def run(self, stock="random", year=-1, file_name="historical_stock_prices.csv", plot_size=30):

        self.bought_index = -1
        self.money_made = 0
        self.time_held = 0
        self.average_sell_interval = 5
        self.buy_num = 0
        self.sell_num = 0
        self.buy_rating_sum = 0
        self.sell_rating_sum = 0
        self.year = year
        self.output_name = OUTPUT_NAME
        self.file_name = file_name
        self.stock = stock
        self.current_index = 0

        if stock == "random":
            self.stock = self.random_stock()

        self.get_stocks()
        self.start_price = float(self.stocks[0]["open"])

        thread = threading.Thread(target=self.buy_sell_thread)
        thread.start()

        plt.ion()
        for i in range(len(self.stocks)):

            self.current_index = i
            x = []
            y = []
            start_loc = max(0, i - plot_size)
            for j in range(start_loc, i):
                x.append(self.stocks[j]["date"])
                y.append(float(self.stocks[j]["open"]))

            plot(x, y, self.stock)
            plt.pause(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock", default="random")
    parser.add_argument("--year", default="-1")
    args = parser.parse_args()
    sim = StockSim()
    sim.run(stock=args.stock, year=str_to_year(args.year))
