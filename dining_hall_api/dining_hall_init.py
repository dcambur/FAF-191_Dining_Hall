import random
from uuid import uuid4


class Table:
    IS_FREE = "IS_FREE"
    ORDER_IS_WAITING = "ORDER_IS_WAITING"
    ORDER_IS_SERVING = "ORDER_IS_SERVING"

    def __init__(self):
        self.status = "FREE"
        self.order = Order()

    def make_order(self, food_ids):
        self.__set_status(self.ORDER_IS_WAITING)
        self.order.set_order(food_ids)

    def __set_status(self, status):
        self.status = status


class Waiter:
    IS_WAITING = "WAITING"
    IS_SERVING = "SERVING"

    def __init__(self):
        self.status = self.IS_WAITING

    @staticmethod
    def find_highest_priority_table(tables):
        return sorted(tables, key=lambda x: x.order.priority)

    def __set_status(self, status):
        self.status = status

    def serve_table(self, tables):
        priority_table = self.find_highest_priority_table(tables)
        if priority_table:
            self.__set_status(self.IS_SERVING)


class Order:
    def __init__(self):
        self.id = str(uuid4())
        self.items = []
        self.priority = None
        self.max_wait = None

    def set_order(self, food_ids):
        self.items = food_ids
        self.priority = random.randrange(1, 5)
        self.max_wait = self.__get_max_wait()

    def get_order_data(self):
        return {"id": str(uuid4()),
                "items": self.items,
                "priority": self.priority,
                "max_wait": self.max_wait}

    def __get_max_wait(self):
        return sorted(self.items, key=lambda x: x["preparation-time"])[
                   0] * 1.3

    def __repr__(self):
        return self.get_order_data()

    def __str__(self):
        return self.get_order_data()


class DiningHall:
    def __init__(self, table_number, food_list):
        self.table_number = table_number
        self.waiter_number = table_number // 2
        self.food_list = food_list
