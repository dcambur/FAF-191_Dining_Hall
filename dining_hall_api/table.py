import random, itertools
from menu import menu
from enum import Enum
from datetime import datetime

class OrderData:
    order_id = itertools.count()
    def __init__(self, table, waiter_id, items, priority, max_wait):
        self.id = next(self.order_id)
        self.table = table
        self.waiter_id = waiter_id
        self.items = items
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = int(datetime.now().timestamp())

    def to_dict(self):
        return {"order_id": self.id,
                "table_id": self.table.id,
                "waiter_id": self.waiter_id,
                "items": self.items,
                "priority": self.priority,
                "max_wait": self.max_wait,
                "pick_up_time": self.pick_up_time}


class TableState(Enum):
    FREE = 1
    WAITING_TO_MAKE = 2
    WAITING_TO_BE_SERVED = 3


class Table:
    table_id = itertools.count()
    def __init__(self):
        self.id = next(self.table_id)
        self.state = TableState.FREE

    def generate_order(self, waiter_id):
        menu_items = [menu[random.randint(0, len(menu) - 1)] for _ in
                    range(random.randint(1, 5))]
        menu_ids = [item["id"] for item in menu_items]
        menu_max_wait = max(
            [item["preparation-time"] for item in menu_items]) * 1.3

        priority = random.randrange(0, 5)
        order_data = OrderData(self, waiter_id, menu_ids, priority, menu_max_wait)

        return order_data
