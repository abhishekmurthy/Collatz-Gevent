import gevent
interval_config = 1000

cycle_count_dict = {1 : 1}

def find_cycle_length(n):
    if cycle_count_dict.has_key(n):
        return cycle_count_dict[n]
    elif n % 2 == 0:
        cycle_count_dict[n] = find_cycle_length(n / 2) + 1
        return cycle_count_dict[n]
    else:
        cycle_count_dict[n] = find_cycle_length(3 * n + 1) + 1
        return cycle_count_dict[n]


def handle_collatz(minimum, maximum):
    large = 0
    if (maximum - minimum == interval_config) and (minimum % interval_config == 1) and (minimum in dic1000):
        return dic1000[minimum]
    else:
        for i in range(minimum, maximum):
            count = find_cycle_length(i)
            if count > large:
                large = count
        return large

def collatz_range(minimum, maximum):
    boundry_start = ((minimum + interval_config) / interval_config) * interval_config
    threads = [gevent.spawn(handle_collatz, minimum, min(boundry_start, maximum) + 1)]
    threads.extend([gevent.spawn(handle_collatz, interval, min(interval + interval_config, maximum + 1)) for interval in xrange(boundry_start + 1, maximum, interval_config)])
    gevent.joinall(threads)

    return max([thread.value for thread in threads])

dic1000 = {}
def precompute_ranges():
    maxrange = 1000000
    for i in xrange(1, maxrange, interval_config):
        dic1000[i] = handle_collatz(i, min(i + interval_config, maxrange))

def unitest_ranges():
#   [ 1 : 1 ]  [ 2 : 2 ]  [ 3 : 8 ]  [ 4 : 3 ]  [ 5 : 6 ]
#   [ 6 : 9 ]  [ 7 : 17 ]  [ 8 : 4 ]  [ 9 : 20 ]  [ 10 : 7 ]
#   [ 11 : 15 ]  [ 12 : 10 ]  [ 13 : 10 ]  [ 14 : 18 ]  [ 15 : 18 ]
#   [ 16 : 5 ]  [ 17 : 13 ]  [ 18 : 21 ]  [ 19 : 21 ]  [ 20 : 8 ]

    assert collatz_range(1, 2) == 2
    assert collatz_range(2, 3) == 8
    assert collatz_range(1, 3) == 8
    assert collatz_range(4, 5) == 6
    assert collatz_range(1, 5) == 8
    assert collatz_range(1, 6) == 9
    assert collatz_range(1, 7) == 17
    assert collatz_range(1, 9) == 20
    assert collatz_range(10, 11) == 15
    assert collatz_range(9, 11) == 20
    assert collatz_range(1, 11) == 20

    assert 179 == collatz_range(1, 1000)
    assert 525 == collatz_range(1, 1000000)

    print "All tests passed"

if __name__ == '__main__':
    unitest_ranges()
