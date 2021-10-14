import threading, queue, itertools, time, requests, json
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

    def _serve_order(self):
        # put the real code here
        pass

    def serve_order(self):
        self.on_thread(self._serve_order)

    def take_order(self):
        for table in self.tables:
            # maybe removed
            time.sleep(0.2)
            with table_locks[table.id]:
                #print(f"waiter id: {self.id}, table id: {table.id}")
                if table.state == TableState.FREE:
                    table.state = TableState.WAITING_TO_MAKE
                    generated_order = table.generate_order(self.id)
                    self.orders.append(generated_order)
                    print(generated_order.to_dict())
                    table.state = TableState.WAITING_TO_BE_SERVED
                    requests.post(config.KITCHEN_URL, json=json.dumps(generated_order.to_dict()))
