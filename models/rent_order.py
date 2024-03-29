from collections import OrderedDict
from models.model import Model
from models.customer import Customer
from models.car import Car
from datetime import datetime


class RentOrder(Model):
    INSURANCE_PERCENT = 0.05
    KM_ALLOWANCE_PER_DAY = 100
    EXTRA_INSURANCE = 4000
    ADDON_PRICE = 450
    DAILY_LATE_FEE = 20000

    def __init__(
            self, order_number: int, car: Car, customer: Customer,
            pickup_time: datetime, estimated_return_time: datetime,
            pickup_branch_name: str, return_branch_name: str,
            include_extra_insurance: bool, base_cost: int,
            remaining_debt: int = -1, kilometers_driven: int = 0,
            return_time: datetime = None, addon_price=0
    ):
        self.__order_number = order_number
        self.__car = car
        self.__customer = customer
        self.__pickup_time = pickup_time
        self.__estimated_return_time = estimated_return_time
        self.__pickup_branch_name = pickup_branch_name
        self.__return_branch_name = return_branch_name
        self.__remaining_debt = remaining_debt
        self.__kilometers_driven = kilometers_driven
        self.__return_time = return_time
        self.__base_cost = base_cost
        self.__insurance_total = int(base_cost * self.INSURANCE_PERCENT)
        self.__extra_insurance_total = 0
        self.__addon_price = addon_price
        if include_extra_insurance:
            self.__extra_insurance_total += self.EXTRA_INSURANCE
        self.__total_cost = base_cost + self.__extra_insurance_total
        self.__total_cost += addon_price
        if remaining_debt == -1:
            self.__remaining_debt = self.__total_cost

    def csv_repr(self):
        rent_order_dict = self.get_dict()
        return_time_str = self.__estimated_return_time.isoformat()
        lpn = self.__customer.get_key()
        rent_order_dict["Bíll"] = self.__car.get_key()
        rent_order_dict["Ökuskírteinisnúmer Viðskiptavinar"] = lpn
        rent_order_dict["Sóttur þann"] = self.__pickup_time.isoformat()
        rent_order_dict["Áætlaður skilatími"] = return_time_str
        if self.__return_time:
            return_time_iso = self.__return_time.isoformat()
            rent_order_dict["Raunverulegur skilatími"] = return_time_iso
        return rent_order_dict

    def get_dict(self):
        return OrderedDict([
            ("Bókunar númer", self.__order_number),
            ("Bíll", self.__car),
            ("Ökuskírteinisnúmer Viðskiptavinar", self.__customer),
            ("Sóttur þann", self.__pickup_time),
            ("Áætlaður skilatími", self.__estimated_return_time),
            ("Sóttur hjá", self.__pickup_branch_name),
            ("Skilaður hjá", self.__return_branch_name),
            ("Auka trygging", self.__extra_insurance_total != 0),
            ("Grunnkostnaður", self.__base_cost),
            ("Eftirstaða borgunar", self.__remaining_debt),
            ("Keyrðir kílómetrar", self.__kilometers_driven),
            ("Raunverulegur skilatími", self.__return_time),
        ])

    def __str__(self):
        pickup_str = str(self.__pickup_time)
        return_str = str(self.__return_time)
        if self.__return_time is None:
            return_str = "Ekki skilað"
        order_string = "Pöntun #{}, Viðskiptavinur: {},\n\tBíll: {},"
        order_string += "\n\tUpphafstími: {}, \n\tSkilatími: {}"
        return order_string.format(
            str(self.__order_number), self.get_customer().get_name(),
            self.__car.get_name(), pickup_str, return_str
        )

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.get_order_number() == other.get_order_number()
        else:
            return self.get_order_number() == str(other)

    # Gets
    def get_order_number(self):
        return self.__order_number

    def get_car(self):
        return self.__car

    def get_customer(self):
        return self.__customer

    def get_pickup_time(self):
        return self.__pickup_time

    def get_pickup_date(self):
        return self.__pickup_time

    def get_estimated_return_time(self):
        return self.__estimated_return_time

    def get_pickup_branch_name(self):
        return self.__pickup_branch_name

    def get_return_branch_name(self):
        return self.__return_branch_name

    def get_insurance_total(self):
        return self.__insurance_total

    def get_extra_insurance_total(self):
        return self.__extra_insurance_total

    def get_total_cost(self):
        return self.__total_cost

    def get_remaining_debt(self):
        return self.__remaining_debt

    def get_kilometers_driven(self):
        return self.__kilometers_driven

    def get_return_time(self):
        return self.__return_time

    def get_key(self):
        return self.__order_number

    def get_name(self):
        return "".join((
            "[", str(self.get_pickup_time().date()), "] ",
            self.get_customer().get_name(),
            ": ",
            self.get_car().get_name()
        ))

    def get_base_cost(self):
        return self.__base_cost

    def get_addon_price(self):
        addon_count = len(self.__car.get_extra_properties())
        return self.ADDON_PRICE * addon_count

    # Sets
    def set_order_number(self, order_number):
        self.__order_number = order_number

    def set_car(self, car):
        self.__car = car

    def set_customer(self, customer):
        self.__customer = customer

    def set_pickup_time(self, pickup_time):
        self.__pickup_time = pickup_time

    def set_estimated_return_time(self, estimated_return_time):
        self.__estimated_return_time = estimated_return_time

    def set_pickup_branch_name(self, pickup_branch_name):
        self.__pickup_branch_name = pickup_branch_name

    def set_return_branch_name(self, return_branch_name):
        self.__return_branch_name = return_branch_name

    def set_insurance_total(self, insurance_total):
        self.__insurance_total = insurance_total

    def set_extra_insurance_total(self, extra_insurance_total):
        self.__extra_insurance_total = extra_insurance_total

    def set_total_cost(self, total_cost):
        self.__total_cost = total_cost

    def set_remaining_debt(self, remaining_debt):
        self.__remaining_debt = remaining_debt

    def set_kilometers_driven(self, kilometers_driven):
        self.__kilometers_driven = kilometers_driven

    def set_return_time(self, return_time):
        self.__return_time = return_time
