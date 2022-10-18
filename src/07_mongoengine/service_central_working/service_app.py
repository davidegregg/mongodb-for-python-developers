from nosql.mongo_setup import global_init
from nosql.car import Car
from nosql.engine import Engine
from nosql.servicehistory import ServiceHistory


def main():
    print_header()
    config_mongo()
    user_loop()


def print_header():
    print('----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.02              |')
    print('|               demo edition                  |')
    print('|                                             |')
    print('----------------------------------------------')
    print()


def config_mongo():
    global_init()


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [p]oorly serviced")
        print(" * [f]ind car")
        print(" * perform [s]ervice")
        print(" * e[x]it")
        print()
        ch = input("> ").strip().lower()
        if ch == 'a':
            add_car()
        elif ch == 'l':
            list_cars()
        elif ch == 'p':
            show_poorly_serviced_cars()
        elif ch == 'f':
            find_car()
        elif ch == 's':
            service_car()
        elif not ch or ch == 'x':
            print("Goodbye")
            break


def add_car():
    model = input("What is the model? ")
    make = input("What is the make? ")
    year = int(input("Year built? "))

    car = Car()
    car.model = model
    car.make = make
    car.year = year

    engine = Engine()
    engine.horsepower = 590
    engine.mpg = 22
    engine.liters = 4.0
    car.engine = engine

    car.save()


def list_cars():
    cars = Car.objects().order_by("-year")

    for car in cars:
        print("{} -- {} with vin {} (year {})".format(car.make, car.model, car.vin, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * ${:,.0f}: {}".format(s.price, s.description))


def find_car():
    print("TODO: find_car")


def service_car():
    vin = input("What is the VIN of the car to service? ")

    service = ServiceHistory()
    service.price = float(input("What is the price? "))
    service.description = input("What type of service is this? ")
    service.customer_rating = int(input("How happy is our customer? [1-5] "))

    updated = Car.objects(vin=vin).update_one(push__service_history=service)
    if updated == 0:
        print("Car with VIN {} not found!".format(vin))
        return


def show_poorly_serviced_cars():
    level = int(input("What max level of satisfaction are we looking for? [1-5] "))
    cars = Car.objects(service_history__customer_rating__lte=level)
    for car in cars:
        print("{} -- {} with vin {} (year {})".format(
            car.make, car.model, car.vin, car.year))
        print("{} of service records".format(len(car.service_history)))
        for s in car.service_history:
            print("  * Satisfaction: {} ${:,.0f} {}".format(
                s.customer_rating, s.price, s.description))
    print()


if __name__ == '__main__':
    main()
