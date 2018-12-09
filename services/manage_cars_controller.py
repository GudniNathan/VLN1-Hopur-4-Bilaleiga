from services.controller import Controller
from repositories.car_repository import CarRepository
from ui.menu import Menu
from models.admin import Admin


class ManageCarsController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Bílaskrá"
        self.__car_repo = CarRepository()
        self.__selected_car = None
        self._menu_stack.append(self.__make_main_menu())

    # Operations
    def go_to_search(self, values, menu):
        results = self.__search_cars(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_customer
        )
        self._menu_stack.append(search_menu)

    def go_to_search_all(self, values, menu):
        for i in range(len(values)):
            values[i] = ""
        self.go_to_search(values, menu)

    def go_to_create(self, values, menu):
        type_str = "Bílinn"
        fields = self.__car_repo.get_row_names()
        new_car_menu = self._ui.get_new_model_object_menu(
            self.__controller_header, fields, type_str
        )
        self._menu_stack.append(new_car_menu)

    def select_car(self, car, menu):
        customer_menu = self._ui.get_model_object_options_menu(
            car, car.get_licence_plate_number(), self.__controller_header,
            self.go_to_edit, self.go_to_delete
        )
        self.__selected_car = car
        self._menu_stack.append(car)

    def go_to_edit(self, values, menu):
        car = self.__selected_car
        name = car.get_licence_plate_number()
        edit_menu = self._ui.get_edit_menu(
            car, name, self.__controller_header, self.edit_car
        )
        self._menu_stack.append(edit_menu)

    def edit_selected_customer(self, values, menu):
        # Update the salesperson
        old_customer = self.__selected_customer
        old_key = old_customer.get_drivers_license_id()
        try:
            customer = self._validation.validate_customer(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        self.__customer_repo.update(customer, old_key)
        # Move to feedback screen
        update_report_menu = self._ui.get_edit_report_menu(
            customer, self.__controller_header, self.restart
        )
        self._menu_stack.append(update_report_menu)

    # Menus - try to move these to the ui layer
    def __make_main_menu(self):
        header = self.__controller_header
        header += "\n\nLeita að bíl"
        inputs = [{"prompt": "Númeraplata:"},
                  {"prompt": "Flokkur:"},
                  {"prompt": "Fjöldi sæta:"},
                  {"prompt": "Fjöldi dyra:"},
                  {"prompt": "Birta lausa (J/N):"},
                  {"prompt": "Í útleigu (J/N):"}]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá alla bíla", "value": search_all},
        ]
        if type(self._service.get_current_user()) == Admin:
            add_car_option = {"description": "Bæta við bíl", "value": create}
            options.append(add_car_option)
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(
            header=header, inputs=inputs, options=options, footer=footer,
            can_submit=False, back_function=self.back, stop_function=self.stop,
            max_options_per_page=10
        )
        return menu
