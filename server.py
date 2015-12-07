from json import loads, dumps
from flask import Flask, request
import gevent
from gevent import monkey
app = Flask(__name__)

@app.route("/")
def collatz():
    minimum = int(request.args.get('min' ,''))
    maximum = int(request.args.get('max', ''))
    if (minimum > maximum) or (maximum > 1000000):
        return format_failure(minimum, maximum)
    out = handle_collatz(minimum, maximum)
    return format_success(minimum, maximum, out)

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

def collatz(n):
    if cycle_count_dict.has_key(n):
        return cycle_count_dict[n]
    elif n % 2 == 0:
        cycle_count_dict[n] = collatz(n / 2) + 1
        return cycle_count_dict[n]
    else:
        cycle_count_dict[n] = collatz(3 * n + 1) + 1
        return cycle_count_dict[n]

def handle_collatz(minimum, maximum):
    '''
    threads = map(lambda n : gevent.spawn(collatz, n), xrange(minimum, maximum + 1))
    gevent.joinall(threads)
    return max([thread.value for thread in threads])
    '''
    large = 0
    for i in range(minimum, maximum + 1):
        count = collatz(i)
        if count > large:
            large = count
    return large

if __name__ == '__main__':
    monkey.patch_all()
    app.debug = True
    app.run()
