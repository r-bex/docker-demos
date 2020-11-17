import random
import time

def print_multiple():
    num_options = list(range(1,13))
    x = random.choice(num_options)
    y = random.choice(num_options)
    z = x * y
    print "{} x {} = {}".format(x,y,z)

if __name__ == "__main__":
    while True:
        print_multiple()
        time.sleep(1)