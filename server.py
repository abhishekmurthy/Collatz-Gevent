import collatz
from json import loads, dumps
from flask import Flask, request
import gevent
from gevent import monkey
app = Flask(__name__)

@app.route("/")
def collatz_range():
    minimum = int(request.args.get('min' ,''))
    maximum = int(request.args.get('max', ''))

    if (minimum > maximum) or (maximum > 1000000):
        return format_failure(minimum, maximum)

    out = collatz.collatz_range(minimum, maximum)

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

if __name__ == '__main__':
    collatz.precompute_ranges()
    monkey.patch_all()
    #app.debug = True
    app.run()
