import sys
import matplotlib.pyplot as plt
import time
import numpy as np
import threading

x = 0

def buy_sell_thread():
    print(x)

def run():
    global x
    x = 1
    thread = threading.Thread(target=buy_sell_thread)
    thread.start()

run()
