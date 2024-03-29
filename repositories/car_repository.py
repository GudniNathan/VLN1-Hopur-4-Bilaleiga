from repositories.repository import Repository
from repositories.branch_repository import BranchRepository
from repositories.price_list_repository import PriceListRepository
from models.car import Car


class CarRepository(Repository):
    _FILENAME = "./data/Cars.csv"
    _TYPE = Car
    _PRIMARY_KEY = "Bílnúmer"  # name of primary key
    _CSV_ROW_NAMES = [
        "Bílnúmer", "Gerð", "Flokkur", "Fjöldi hjóla",
        "Drif", "Sjálfskiptur", "Fjöldi sæta",
        "Aðrir eiginleikar", "Kílómetrafjöldi", "Núverandi útibú"
    ]

    def dict_to_model_object(self, car_dict):
        '''Translates the read csv dictionary to a car object.'''
        license_plate_number = car_dict['Bílnúmer']
        model = car_dict['Gerð']
        category = PriceListRepository().get(car_dict["Flokkur"])
        wheel_count = int(car_dict["Fjöldi hjóla"])
        drivetrain = car_dict["Drif"]
        automatic_transmission = car_dict['Sjálfskiptur'] == "True"
        seat_count = int(car_dict['Fjöldi sæta'])
        extra_properties = car_dict['Aðrir eiginleikar'].split(",")
        for i, prop in enumerate(extra_properties):
            extra_properties[i] = prop.strip()
        extra_properties = set(extra_properties)
        kilometer_count = int(car_dict['Kílómetrafjöldi'])
        current_branch = BranchRepository().get(car_dict['Núverandi útibú'])
        return Car(
            license_plate_number, model, category, wheel_count, drivetrain,
            automatic_transmission, seat_count, extra_properties,
            kilometer_count, current_branch
        )
