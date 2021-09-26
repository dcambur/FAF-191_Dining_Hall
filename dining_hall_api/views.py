from flask import Blueprint

dining_hall = Blueprint("kitchen", "__name__")


@dining_hall.route("/distribution")
def dining_distribution_test():
    return {"msg": "test response"}, 200
