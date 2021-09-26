import random
import time
from uuid import uuid4
from food import food_list


class Order:
    def __init__(self, items):
        self.id = str(uuid4())
        self.items = items
        self.priority = random.randrange(1, 5)
        self.max_wait = self.__get_max_wait()

    def get_order_data(self):
        return {"id": str(uuid4()),
                "items": self.__get_items_id(),
                "priority": self.priority,
                "max_wait": self.max_wait}

    def __get_items_id(self):
        return [item["id"] for item in self.items]

    def __get_max_wait(self):
        return sorted(self.items, key=lambda x: x["preparation-time"])[
                   0]['preparation-time'] * 1.3

    def __repr__(self):
        return self.get_order_data()

    def __str__(self):
        return self.get_order_data()


class Table:
    IS_FREE = "IS_FREE"
    IS_READY_TO_ORDER = "IS_READY_TO_ORDER"
    IS_WAITING_FOR_ORDER = "IS_WAITING_FOR_ORDER"

    def __init__(self):
        self.status = self.IS_FREE
        self.order = None

    def generate_order(self, food):
        self.order = Order(food)
        self.__set_status(self.IS_READY_TO_ORDER)

        return self.order

    def pass_order(self):
        self.__set_status(self.IS_WAITING_FOR_ORDER)

    def resolve_order(self):
        self.order = None
        self.__set_status(self.IS_FREE)

    def get_current_order(self):
        return self.order

    def __set_status(self, status):
        self.status = status


class Waiter:
    IS_WAITING = "WAITING"
    IS_SERVING = "IS_SERVING"

    def __init__(self):
        self.status = self.IS_WAITING
        self.serving_table = None

    @staticmethod
    def find_highest_priority_table(tables):
        priority_table = None
        max_priority = 0
        for table in tables:
            if table.status == table.IS_READY_TO_ORDER:
                if max_priority < table.order.priority:
                    max_priority = table.order.priority
                    priority_table = table

        return priority_table

    def __set_status(self, status):
        self.status = status

    def serve_table_order(self, tables):
        self.serving_table = self.find_highest_priority_table(tables)
        if self.serving_table:
            self.__set_status(self.IS_SERVING)

    def resolve_order(self):
        self.__set_status(self.IS_WAITING)
        self.serving_table.resolve_order()
        self.serving_table = None


class DiningHall:
    def __init__(self, table_quantity, food_list):
        self.table_quantity = table_quantity
        self.waiter_quantity = table_quantity // 2
        self.food_list = food_list
        self.tables = [self.__create_table() for _ in
                       range(self.table_quantity)]
        self.waiters = [self.__create_waiter() for _ in
                        range(self.waiter_quantity)]

    @staticmethod
    def __create_table():
        return Table()

    @staticmethod
    def __create_waiter():
        return Waiter()

    def __get_random_food(self):
        split_left = random.randrange(0, len(self.food_list) // 2)
        split_right = random.randrange(len(self.food_list) // 2,
                                       len(self.food_list))

        return self.food_list[split_left:split_right]

    def __get_random_food_ids(self):
        return [food["id"] for food in self.__get_random_food()]

    def __get_free_table(self):
        for table in self.tables:
            if table.status == table.IS_FREE:
                return table
        return None

    def __get_ready_table(self):
        for table in self.tables:
            if table.status == table.IS_READY_TO_ORDER:
                return table
        return None

    def __get_served_table(self):
        for table in self.tables:
            if table.status == table.IS_WAITING_FOR_ORDER:
                return table
        return None

    def __get_waiting_waiter(self):
        for waiter in self.waiters:
            if waiter.status == waiter.IS_WAITING:
                return waiter
        return None

    def __get_serving_waiter(self):
        for waiter in self.waiters:
            if waiter.status == waiter.IS_SERVING:
                return waiter
        return None

    def create_order(self):
        free_tables = self.__get_free_table()

        if free_tables:
            free_tables.generate_order(self.__get_random_food())

    def process_order(self):
        waiting_waiter = self.__get_waiting_waiter()
        table_to_serve = waiting_waiter.find_highest_priority_table(
            self.tables)

        if table_to_serve:
            waiting_waiter.serve_table_order(table_to_serve)
            table_to_serve.pass_order()

    def finalize_order(self):
        serving_waiter = self.__get_serving_waiter()

        if serving_waiter:
            serving_waiter.resolve_order()


dining_hall = DiningHall(10, food_list)
dining_hall.create_order()
time.sleep(5)
dining_hall.create_order()

for table in dining_hall.tables:
    if not table.order:
        continue

    for key, value in table.order.get_order_data().items():
        print(key, value)
    print()