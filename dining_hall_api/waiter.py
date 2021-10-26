import threading, queue, itertools, time, requests, json, random
from datetime import datetime
import config
from table import TableState

table_locks = []
for _ in range(config.TABLES):
    table_locks.append(threading.Lock())


class Waiter(threading.Thread):
    waiter_id = itertools.count()

    def __init__(self, q, rank, rank_lock, tables=[], orders=[], loop_time = 1.0/60, *args, **kwargs):
        self.q = q
        self.timeout = loop_time
        self.id = next(self.waiter_id)
        self.tables = tables
        self.orders = orders
        self.rank = rank
        self.rank_lock = rank_lock
        super().__init__(*args, **kwargs)

    def on_thread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
            except queue.Empty:
                self.take_order()

    def _serve_order(self, *args, **kwargs):
        time.sleep(random.randint(2, 4) * config.TIME_UNIT)
        order = args[0]
        table_id = order["table_id"]
        order_id = order["order_id"]
        waiter_id = order["waiter_id"]
        if waiter_id == self.id:
            print(f"Order received from kitchen: {order}")
            # FIXME: use locks to prevent races
            for idx, order in enumerate(self.orders):
                if order.id == order_id:
                    order_to_remove = idx
                    break
            if order_to_remove:   
                finished_order = self.orders.pop(order_to_remove)
                print(f"Order removed from order list: {finished_order.to_dict()}")
                self.tables[table_id].state = TableState.FREE
                print(f"Order served: {order_id}, table: {table_id}, waiter: {self.id}")
                order_serve_time = int(datetime.now().timestamp())
                order_total_time = order_serve_time - finished_order["pick_up_time"]
                order_rank = round((order_total_time / finished_order["max_wait"]), 2)
                print(f"Order rank coefficient is: {order_rank}")
                with self.rank_lock:
                    self.rank = round((self.rank + order_rank)/2, 2)
                    print(f"New global rank coefficient is: {self.rank}")
                    if self.rank > 1.4:
                        print("We are 0 star")
                    elif 1.3 < self.rank < 1.4:
                        print("We are 1 star")
                    elif 1.2 < self.rank < 1.3:
                        print("We are 2 stars")
                    elif 1.1 < self.rank < 1.2:
                        print("We are 3 stars")
                    elif 1.0 < self.rank < 1.1:
                        print("We are 4 stars")
                    elif self.rank < 1.0:
                        print("We are 5 stars")
        else:
            print(f"Wrong order received, waiter in order: {waiter_id}, mine id is: {self.id}")

    def serve_order(self, *args, **kwargs):
            self.on_thread(self._serve_order, *args, **kwargs)

    def take_order(self):
        for table in self.tables:
            time.sleep(random.randint(2, 4) * config.TIME_UNIT)
            with table_locks[table.id]:
                if table.state == TableState.FREE:
                    table.state = TableState.WAITING_TO_MAKE
                    generated_order = table.generate_order(self.id)
                    print(f"Order created: {generated_order.to_dict()}")
                    self.orders.append(generated_order)
                    table.state = TableState.WAITING_TO_BE_SERVED
                    requests.post(config.KITCHEN_URL, data=json.dumps(generated_order.to_dict()), headers={"Content-Type": "application/json"})
                    print(f"Order sent to kitchen: {generated_order.to_dict()}")
