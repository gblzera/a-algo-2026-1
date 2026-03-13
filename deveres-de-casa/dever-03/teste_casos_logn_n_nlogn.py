count = 0

# T(n) = T(n/2) + 1 ou + O(1)
def rec1(n):
    global count
    count += 1 # o +1 da recorrencia
    if n <= 1 :
        return
    rec1(n // 2) # a chamada recursiva

# T(n) = T(n/2) + n ou + O(n)
def rec2(n):
    global count
    count += n # o +n da recorrencia
    if n <= 1 :
        return
    rec2(n // 2) # a chamada recursiva

# T(n) = 2T(n/2) + n -> mergeSort
def rec3(n):
    global count
    count += n # o +n da recorrencia
    if n <= 1 :
        return
    rec3(n // 2) # a primeira chamada recursiva
    rec3(n // 2) # a segunda chamada recursiva

import math

sizes = [8, 64, 512, 1024]

for rec, name, expected in [
    (rec1, "T(n/2) + 1  ", "O(log n)"),
    (rec2, "T(n/2) + n  ", "O(n)"),
    (rec3, "2T(n/2) + n ", "O(n log n)")
]:
    print(f"\n--- {name} | {expected} ---")
    for n in sizes:
        count = 0
        rec(n)
        log_n = round(math.log2(n), 1)
        print(f"n={n:5} | count={count:>6} | log n ={log_n} | n log n={round(n * log_n, 1):>6}")