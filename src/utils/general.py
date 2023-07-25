import time
import math
import random


def random_sleep(avg_n_of_seconds):
    sleep_time = random.normalvariate(avg_n_of_seconds,
                                      avg_n_of_seconds ** 0.5)
    time.sleep(math.fabs(sleep_time))


def smart_join(collection, connector="|"):
    try:
        return connector.join(collection)
    except TypeError:
        return None


def smart_cast(object_, type_):
    try:
        return type_(object_)
    except TypeError:
        return None


def smart_slice(collection, idx=0):
    try:
        return collection[idx]
    except IndexError:
        return None
