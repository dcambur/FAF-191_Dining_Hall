import requests
from flask import Blueprint
from .dining_hall_init import DiningHall
from food import food_list

dining_hall = Blueprint("kitchen", "__name__")


@dining_hall.route("/distribution")
def dining_distribution_test():
    hall = DiningHall(table_number=10, food_list=food_list)

    return {"msg": "oke"}, 200
