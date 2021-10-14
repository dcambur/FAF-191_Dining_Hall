import threading, queue, itertools, time, requests, json, random
import config
from table import TableState

table_locks = []
for _ in range(config.TABLES):
    table_locks.append(threading.Lock())


class Waiter(threading.Thread):
    waiter_id = itertools.count()

    def __init__(self, q, tables=[], orders=[], loop_time = 1.0/60, *args, **kwargs):
        self.q = q
        self.timeout = loop_time
        self.id = next(self.waiter_id)
        self.tables = tables
        self.orders = orders
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
        # slowdown waiter's moves a bit
        time.sleep(random.randint(2, 4) * config.TIME_UNIT)
        order = args[0]
        print(f"Order received from kitchen: {order}")
        table_id = order["table_id"]
        order_id = order["order_id"]
        print(self.orders.pop(order_id).to_dict())
        self.tables[table_id].state = TableState.FREE

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
                    requests.post(config.KITCHEN_URL, json=json.dumps(generated_order.to_dict()))
                    print(f"Order sent to kitchen: {generated_order.to_dict()}")
