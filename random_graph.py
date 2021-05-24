#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt

def plot(x, y, stock):
        plt.clf()
        _ = plt.plot(x, y)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Price of " + stock + " over time")
        plt.draw()

data = [100]
x = [1]

for i in range(30):
    x.append(x[len(x) - 1] + 1)
    data.append(data[len(data) - 1] + random.randint(-10, 10))

plot(x, data, "AAPL")
plt.pause(20)
