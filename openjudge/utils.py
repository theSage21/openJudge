import random


def random_string(n=15):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz')
                    for _ in range(n)])
