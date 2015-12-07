from json import loads, dumps
from flask import Flask, request
import gevent
from gevent import monkey
app = Flask(__name__)

interval_config = 10000
@app.route("/")
def collatz():
    minimum = int(request.args.get('min' ,''))
    maximum = int(request.args.get('max', ''))

    if (minimum > maximum) or (maximum > 1000000):
        return format_failure(minimum, maximum)

    out = collatz_range(minimum, maximum)

    return format_success(minimum, maximum, out)

def collatz_range(minimum, maximum):

    threads = [ gevent.spawn(handle_collatz, interval, min(interval + interval_config, maximum)) for interval in xrange(minimum, maximum, interval_config) ]
    gevent.joinall(threads)

    return max([thread.value for thread in threads])

def format_failure(minimum, maximum):
    result = {}
    result['minimum'] = minimum
    result['maximum'] = maximum
    result['status'] = 'failure'
    result['description'] = 'Minimum has to be lesser than maximum and maximum must be within 10,00,000'
    return dumps(result)

def format_success(minimum, maximum, out):
    result = {}
    result['minimum'] = minimum
    result['maximum'] = maximum
    result['Maximum Cycle Count'] = out
    result['status'] = 'success'
    return dumps(result)

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
    for i in range(minimum, maximum + 1):
        count = find_cycle_length(i)
        if count > large:
            large = count
    return large

def unittests():
    assert 8 == collatz_range(1, 3)
    assert 2 == collatz_range(1, 2)
    assert 179 == collatz_range(1, 1000)
    assert 525 == collatz_range(1, 1000000)

    print "All tests passed"
if __name__ == '__main__':
    unittests()
    monkey.patch_all()
    app.debug = True
    app.run()
