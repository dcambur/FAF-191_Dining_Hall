import threading, queue, time
from datetime import datetime
from flask import Flask, request
import config
import table
from waiter import Waiter


# init
orders = []
tables = []
waiters = []
waiter_pipes = []
rank = 0

app = Flask(__name__)

@app.route('/distribution', methods=['POST'])
def distributor():
    global rank
    if request:
        r = request.get_json(force=True)
        if r["waiter_id"]:
            waiter_id = r["waiter_id"]
            waiters[waiter_id].serve_order(r)
            order_serve_time = int(datetime.now().timestamp())
            order_total_time = order_serve_time - r["pick_up_time"]
            order_rank = round((order_total_time / r["max_wait"]), 2)
            print(f"Old rank coefficient: {rank}")
            print(f"Order rank coefficient is: {order_rank}")
            if rank == 0:
                print("It's only begging of the day")
                rank = order_rank
            else:
                rank = round((rank + order_rank)/2, 2)
            print(f"New global rank coefficient is: {rank}")
            if rank >= 1.4:
                print("We are 0 star")
            elif 1.3 < rank < 1.4:
                print("We are 1 star")
            elif 1.2 < rank < 1.3:
                print("We are 2 stars")
            elif 1.1 < rank < 1.2:
                print("We are 3 stars")
            elif 1.0 < rank < 1.1:
                print("We are 4 stars")
            elif rank < 1.0:
                print("We are 5 stars")

    return "Ok"

if __name__ == "__main__":
    # start distributor
    distributor_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False))
    distributor_thread.daemon = True
    distributor_thread.start()

    # prepare tables
    for _ in range(config.TABLES):
        new_table = table.Table()
        tables.append(new_table)

    # start waiters
    for _ in range(config.WAITERS):
        pipe = queue.Queue()
        waiter = Waiter(pipe, tables=tables, orders=orders)
        waiter.daemon = True
        waiters.append(waiter)
        waiter_pipes.append(pipe)
        waiter.start()

    try:
        while True:
            for t in waiters:
                if t.exception:
                    # thread raised an exception
                    raise t.exception
            time.sleep(0.2)

    except Exception as e:
        print("Exception in main thread")

    finally:
        for t in waiters:
            # stop the threads
            t.stop()
