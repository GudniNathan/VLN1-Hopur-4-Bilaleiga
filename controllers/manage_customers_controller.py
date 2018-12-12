from controllers.controller import Controller
from repositories.customer_repository import CustomerRepository
from ui.menu import Menu


class ManageCustomersController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Viðskiptavinaskrá"
        self.__customer_repo = CustomerRepository()
        self.__selected_customer = None
        if shortcut_to_register:
            self.go_to_create(None, None)
        else:
            self._menu_stack.append(self.__make_main_menu())

    # Operations
    def go_to_search(self, values, menu):
        results = self.__search_customers(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_customer
        )
        self._menu_stack.append(search_menu)

    def go_to_create(self, values, menu):
        type_str = "Viðskiptavininn"
        fields = self.__customer_repo.get_row_names()
        new_customer_menu = self._ui.get_new_model_object_menu(
            self.__controller_header, fields, type_str, self.create_customer
        )
        self._menu_stack.append(new_customer_menu)

    def select_customer(self, customer, menu):
        customer_menu = self._ui.get_model_object_options_menu(
            customer, customer.get_name(), self.__controller_header,
            self.go_to_edit, self.go_to_delete
        )
        self.__selected_customer = customer
        self._menu_stack.append(customer_menu)

    def go_to_edit(self, values, menu):
        customer = self.__selected_customer
        name = customer.get_name()
        edit_menu = self._ui.get_edit_menu(
            customer, name, self.__controller_header,
            self.edit_selected_customer
        )
        self._menu_stack.append(edit_menu)

    def go_to_delete(self, values, menu):
        customer = self.__selected_customer
        deletion_menu = self._ui.get_deletion_menu(
            customer, customer.get_name(), self.__controller_header,
            self.delete_selected_customer
        )
        self._menu_stack.append(deletion_menu)

    def delete_selected_customer(self, values, menu):
        # delete the salesperson
        self.__customer_repo.remove(self.__selected_customer)
        # create deletion feedback menu
        # the menu should be a special no-back menu
        # go to deletion feedback screen
        delete_feedback_menu = self._ui.get_delete_feedback_menu(
            self.__selected_customer.get_name(),
            self.__controller_header, self.restart
        )
        self.__selected_customer = None
        self._menu_stack.append(delete_feedback_menu)

    def edit_selected_customer(self, values, menu):
        # Update the salesperson
        old_customer = self.__selected_customer
        old_key = old_customer.get_driver_license_id()
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

    def create_customer(self, values, menu):
        try:
            customer = self._validation.validate_customer(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        self.__customer_repo.add(customer)
        new_report_menu = self._ui.get_creation_report_menu(
            customer, self.__controller_header, self.restart
        )
        self._menu_stack.append(new_report_menu)

    # Menus
    def __make_main_menu(self):
        header = self.__controller_header
        header += "\n\nLeita að vidskiptavini"
        inputs = [{"prompt": "Ökuskírteinisnúmer:"},
                  {"prompt": "Kennitala:"},
                  {"prompt": "Nafn:"}]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá alla viðskiptavini", "value": search_all},
            {"description": "Bæta við viðskiptavini", "value": create},
        ]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(header=header, inputs=inputs,
                    options=options, footer=footer, can_submit=False,
                    back_function=self.back, stop_function=self.stop)
        return menu

    def __make_new_customer_menu(self):
        header = self.__controller_header + " -> Nýr viðskiptavinur"
        header += "\nSláðu inn upplýsingarnar fyrir nýja viðskiptavininn:"
        inputs = [
            {"prompt": "driver license id"},
            {"prompt": "personal id"},
            {"prompt": "first name"},
            {"prompt": "last_name"},
            {"prompt": "first birthdate", "type": "date"},
            {"prompt": "phone number"},
            {"prompt": "email"},
        ]
        new_customer_menu = Menu(header=header, inputs=inputs,
                                 back_function=self.back,
                                 stop_function=self.stop,
                                 submit_function=self.create_customer)
        return new_customer_menu

    # Other
    def __search_customers(self, username="", name="", email="", phone=""):
        salespeople = self.__customer_repo.get_all()
        username = username.strip()
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        for i in range(len(salespeople) - 1, -1, -1):
            person = salespeople[i]
            if username and username != person.get_username():
                salespeople.pop(i)
            elif name and name != person.get_name():
                salespeople.pop(i)
            elif email and email != person.get_email():
                salespeople.pop(i)
            elif phone and phone != person.get_phone():
                salespeople.pop(i)
        return salespeople