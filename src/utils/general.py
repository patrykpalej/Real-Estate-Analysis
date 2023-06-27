import time
import math
import random


def random_sleep(avg_n_of_seconds):
    sleep_time = random.normalvariate(avg_n_of_seconds,
                                      avg_n_of_seconds ** 0.5)
    time.sleep(math.fabs(sleep_time))
