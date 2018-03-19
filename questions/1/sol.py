from itertools import islice
def primes():
    primes = [2]
    yield 2
    i = 3
    while True:
        if not any([i % k == 0 for k in primes]):
            primes.append(i)
            yield i
        i += 1


n = int(input())
for i in islice(primes(), n):
    print(i)
