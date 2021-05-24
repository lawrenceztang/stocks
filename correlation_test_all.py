#!/usr/bin/env python3

import csv
import argparse
import os

STOCK_FILE_NAME = "historical_stock_prices.csv"


LEN_PREV = 3

def main():
    file = open("all_stocks", "w+")
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["ticker", "av_gain_positive", "av_gain_turn", "av_gain"])

    csvfile = open(STOCK_FILE_NAME)
    reader = csv.DictReader(csvfile)
    prev_price_dict = {}
    av_gain_turn_dict = {}
    count_turn_dict = {}
    av_gain_pos_dict = {}
    count_pos_dict = {}

    av_gain_dict = {}
    count_dict = {}

    for i in reader:
        
        if not i["ticker"] in prev_price_dict:
            prev_price_dict[i["ticker"]] = []
            av_gain_turn_dict[i["ticker"]] = 0
            count_turn_dict[i["ticker"]] = 0
            av_gain_pos_dict[i["ticker"]] = 0
            count_pos_dict[i["ticker"]] = 0
            av_gain_dict[i["ticker"]] = 0
            count_dict[i["ticker"]] = 0

        if len(prev_price_dict[i["ticker"]]) > LEN_PREV and prev_price_dict[i["ticker"]][LEN_PREV - 1] - prev_price_dict[i["ticker"]][LEN_PREV - 2] > 0:
            av_gain_pos_dict[i["ticker"]] += float(i["open"]) - prev_price_dict[i["ticker"]][LEN_PREV - 1]
            count_pos_dict[i["ticker"]] += 1

        if len(prev_price_dict[i["ticker"]]) > LEN_PREV and prev_price_dict[i["ticker"]][LEN_PREV - 1] - prev_price_dict[i["ticker"]][LEN_PREV - 2] > 0 and prev_price_dict[i["ticker"]][LEN_PREV - 2] - prev_price_dict[i["ticker"]][LEN_PREV - 3] < 0:
            av_gain_turn_dict[i["ticker"]] += float(i["open"]) - prev_price_dict[i["ticker"]][LEN_PREV - 1]
            count_turn_dict[i["ticker"]] += 1

        if len(prev_price_dict[i["ticker"]]) > LEN_PREV and len(prev_price_dict[i["ticker"]]) > 0:
            av_gain_dict[i["ticker"]] += float(i["open"]) - prev_price_dict[i["ticker"]][LEN_PREV - 1]
            count_dict[i["ticker"]] += 1

        if len(prev_price_dict[i["ticker"]]) > LEN_PREV:
            prev_price_dict[i["ticker"]].pop(0)
        prev_price_dict[i["ticker"]].append(float(i["open"]))

    for i in av_gain_turn_dict:
        writer.writerow([i, av_gain_pos_dict[i] / count_pos_dict_dict[i], av_gain_turn_dict[i] / count_turn_dict[i], av_gain_dict[i] / count_dict[i]])



if __name__ == "__main__":
    main()
