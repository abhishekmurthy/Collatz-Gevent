"""
3n+1 Problem
Cycle length of each number is calculated recursively and stored in the hash
table(HT). If any input reduces to a number present in the HT, that values is
used to calculate the cycle length and the recursive function is stopped.
"""

import gevent
collatz_dict = {1 : 1}

def memorized_collatz(n):
    """
    Recursively calculates the Collatz cycle length of number 'n'.
    Results are stored in a HT and will be used when called subsequently.
    """
    if collatz_dict.has_key(n):
        return collatz_dict[n]
    elif n%2 == 0:
        collatz_dict[n] = memorized_collatz(n/2) +1
        return collatz_dict[n]
    else:
        collatz_dict[n] = memorized_collatz(3*n+1) + 1
        return collatz_dict[n]

def range_collatz(range):
    """
    For a given range, return the max cycle length of any number in that range.
    Cycle length of each number in that range is calculated *serially*. Range
    is a tuple of form (min, max)
    """
    (Min, Max) = range
    result = map(lambda n : memorized_collatz(n),
                 xrange(Min, Max+1))
    return max(result)

'''
def p_range_collatz(range):
    """
    For a given range, return the max cycle length of any number in that range.
    Cycle length of each number in that range is calculated *concurrently*. Range
    is a tuple of form (min, max)
    """
    (Min, Max) = range
    threads = map(lambda n : gevent.spawn(memoized_collatz, n),
                  xrange(Min, Max+1))
    gevent.joinall(threads)
    return max([thread.value for thread in threads])
'''

def p_collatz(minimum, maximum):
    return range_collatz([int(minimum), int(maximum)])
