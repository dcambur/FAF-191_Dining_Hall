import threading, queue
import config
import table
from waiter import Waiter
from flask import Flask, request

#from distributor import app

# init
orders = []
tables = []
waiters = []
waiter_pipes = []

app = Flask(__name__)

@app.route('/distribution', methods=['POST'])
def distributor():
    if request:
        r = request.get_json(force=True)

        print(r)
    print(waiters)
    return "Ok"

if __name__ == "__main__":
    # start distributor
    distributor_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False))
    distributor_thread.start()
    # prepare tables
    for _ in range(config.TABLES):
        new_table = table.Table()
        tables.append(new_table)

    # start waiters
    for _ in range(config.WAITERS):
        pipe = queue.Queue()
        waiter = Waiter(pipe, tables=tables, orders=orders)
        waiter.start()
        waiters.append(waiter)
        waiter_pipes.append(pipe)

    for w in waiters:
        w.join()

    distributor_thread.join()
