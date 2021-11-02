import threading, queue, itertools, time, requests, json, random
import config
from table import TableState, OrderState

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
        self.name = f"Waiter-{self.id}"

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
        # time.sleep(random.randint(2, 4) * config.TIME_UNIT)
        order = args[0]
        table_id = order["table_id"]
        order_id = order["order_id"]
        waiter_id = order["waiter_id"]

        if waiter_id == self.id:
            print(f"Order received from kitchen: {order}")
            for order in self.orders:
                if order.id == order_id:
                    order.state = OrderState.SERVED
                    self.tables[table_id].state = TableState.FREE
                    print(f"Order served: {order_id}, table: {table_id}, waiter: {self.id}")
                    break
        else:
            print(f"Wrong order received, waiter in order: {waiter_id}, my id is: {self.id}")

    def serve_order(self, *args, **kwargs):
            self.on_thread(self._serve_order, *args, **kwargs)

    def take_order(self):
        for table in self.tables:
            time.sleep(random.randint(2, 4) * config.TIME_UNIT)
            if table_locks[table.id].acquire(blocking=False):
                if table.state == TableState.FREE:
                    table.state = TableState.WAITING_TO_MAKE
                    generated_order = table.generate_order(self.id)
                    print(f"Order created: {generated_order.to_dict()}")
                    self.orders.append(generated_order)
                    requests.post(config.KITCHEN_URL, data=json.dumps(generated_order.to_dict()), headers={"Content-Type": "application/json"})
                    print(f"Order sent to kitchen: {generated_order.to_dict()}")
                    table.state = TableState.WAITING_TO_BE_SERVED
                table_locks[table.id].release()
