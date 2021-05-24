from selenium import webdriver
from datetime import date
import time

def main(stock):
    file = open(stock, "a")
    prev_minute = -1

    while True:
        now = datetime.now()

        if now.time().minute - prev_minute >= 1 or (prev_minute == 59 and now.time().minute != 59):
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            file.write(dt_string + " " + )

        prev_minute = now.time().minute




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock", default="GOOGL")
    args = parser.parse_args()
    main(stock)
