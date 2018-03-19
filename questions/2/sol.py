def fib(n, cache={}):
    if n <= 2:
        return 1
    if n not in cache:
        cache[n] = fib(n-1) + fib(n-2)
    return cache[n]


print(fib(int(input())))
