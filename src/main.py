####################
# [iShop]  ver 0.1 #
####################
import prettytable as pt


class Code:
    """
    Class: Running Result Status Code
    """
    # Succeeded
    SUCCESS = 0
    # Failed: internal error
    FAIL_INTERNAL_ERROR = 1
    # Failed: wrong username or password
    FAIL_WRONG_USERNAME_OR_PASSWORD = 1
    # Failed: item not found
    FAIL_ITEM_NOT_FOUND = 2
    # Failed: item already exists
    FAIL_ITEM_ALREADY_EXISTS = 3
    # Failed: illegal username
    FAIL_ILLEGAL_USERNAME = 4
    # Failed: illegal item number
    FAIL_ILLEGAL_NUMBER = 5


class Item:
    """
    Class: Item
    """
    def __init__(self, name: str = '', price: float = 0.0, unit: str = ''):
        """
        :param name: name of the item
        :param price: price of the item
        :param unit: unit of the item
        """
        self.name = name
        self.price = price
        self.unit = unit


class User:
    """
    Class: User
    """
    def __init__(self, username: str, password: str = ''):
        """
        :param username: username of the user
        :param password: password of the user
        """
        self.username = username
        self.password = password
        self.shopping_list = []

    def insert_item(self, item: Item, number: float) -> int:
        """ insert new item into the shopping list
        :param item: new item to insert
        :param number: number of new item
        :return: running result status code
        """
        if item and number >= 0:
            # check whether item already exists
            for i in range(len(self.shopping_list)):
                if self.shopping_list[i]['item'] == item:
                    return Code.FAIL_ITEM_ALREADY_EXISTS
            # insert item into list
            self.shopping_list.append({'item': item, 'number': number})
            return Code.SUCCESS
        else:
            return Code.FAIL_INTERNAL_ERROR

    def delete_item(self, item: Item) -> int:
        """ delete selected item from the shopping list
        :param item: selected item to delete
        :return: running result status code
        """
        if item:
            # check whether selected item exists
            # if exists, delete item from list
            for i in range(len(self.shopping_list)):
                if self.shopping_list[i]['item'] == item:
                    self.shopping_list.pop(i)
                    return Code.SUCCESS
            # item not found
            return Code.FAIL_ITEM_NOT_FOUND
        else:
            return Code.FAIL_INTERNAL_ERROR

    def modify_item(self, item: Item, number: float) -> int:
        """ modify the number of selected item in the shopping list
        :param item: selected item to modify
        :param number: new item number
        :return: running result status code
        """
        if item and number >= 0:
            # check whether selected item exists
            # if exists, modify the number
            for i in range(len(self.shopping_list)):
                if self.shopping_list[i]['item'] == item:
                    self.shopping_list[i]['number'] = number
                    return Code.SUCCESS
            # item not found
            return Code.FAIL_ITEM_NOT_FOUND
        else:
            return Code.FAIL_INTERNAL_ERROR

    def clear_item(self) -> int:
        """ clear the shopping list
        :return: running result status code
        """
        self.shopping_list.clear()
        return Code.SUCCESS

    def print_list(self):
        """ print the shopping list
        """
        # create table with PrettyTable
        table = pt.PrettyTable()
        table.field_names = ['Name', 'Price', 'Number', 'Total']
        # add items into the table as rows
        for i in range(len(self.shopping_list)):
            table.add_row([
                # Name
                self.shopping_list[i]['item'].name,
                # Price
                str(self.shopping_list[i]['item'].price) + ' / ' + self.shopping_list[i]['item'].unit,
                # Number
                str(self.shopping_list[i]['number']),
                # Total
                round(self.shopping_list[i]['item'].price * self.shopping_list[i]['number'], 2),
            ])
        # add the sum of all items as the last row
        table.add_row(['', '', '', self.calculate_sum()])
        # print the table
        print(table)

    def calculate_sum(self) -> float:
        """ calculate the sum of items in the shopping list
        :return: sum of items in the shopping list
        """
        item_sum = 0.00
        for i in range(len(self.shopping_list)):
            item_sum += round(self.shopping_list[i]['item'].price * self.shopping_list[i]['number'], 2)
        return item_sum


class Manager:
    """
    Class: Program Manager
    """
    USER_OFFLINE_STATUS = 0  # status code when user not logged in
    USER_ONLINE_STATUS = 1   # status code when user logged in
    ADMIN_ONLINE_STATUS = 2  # status code when admin logged in

    def __init__(self, username: str, password: str = ''):
        """
        :param username: username of the admin
        :param password: password of the admin
        """
        self.item_list = []
        self.user_list = []
        self.admin_username = username
        self.admin_password = password
        self.current_user = None
        self.current_status = Manager.USER_OFFLINE_STATUS

    def run(self):
        """ run shopping system
        """
        # ***** Load *****
        self.current_status = Manager.USER_OFFLINE_STATUS
        self.load()
        # ***** Loop *****
        while True:
            user_input = input()
            if self.current_status == Manager.USER_OFFLINE_STATUS:
                # *** Handle User Offline ***
                while user_input != 'exit':
                    if user_input == '':
                        pass
                    user_input = input()
                else:
                    break

            elif self.current_status == Manager.USER_ONLINE_STATUS:
                # *** Handle User Online ***
                while user_input != 'exit':
                    break
                else:
                    break
            elif self.current_status == Manager.ADMIN_ONLINE_STATUS:
                # *** Handle Admin Online ***
                while user_input != 'exit':
                    break
                else:
                    break
        # ***** Save *****
        self.save()

    def help(self):
        """ print hint for user
        """
        if self.current_status == Manager.USER_OFFLINE_STATUS:
            # print hint for user not logged in
            print('**********')
            print('<logon>:  user register')
            print('<login>:  user login')
            print('<help>:   print hint')
            print('<exit>:   exit program')
        elif self.current_status == Manager.USER_ONLINE_STATUS:
            # print hint for user logged in
            print('<logout>: user logout')
            print('<help>:   print hint')
            print('<exit>:   exit program')
        elif self.current_status == Manager.ADMIN_ONLINE_STATUS:
            # print hint for admin logged in
            print('<logout>: user logout')
            print('<help>:   print hint')
            print('<exit>:   exit program')

    def load(self):
        pass

    def save(self):
        pass

    def logon(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    def search_item(self, name: str) -> Item or None:
        """ search for item by name in the item list
        :param name: name of the item
        :return: item found or None if not found
        """
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                return self.item_list[i]
        return None

    def insert_item(self, name: str, price: float, unit: str) -> int:
        """ insert new item into the item list
        :param name: name of the new item to insert
        :param price: price of the new item to insert
        :param unit: unit of the new item to insert
        :return: running result status code
        """
        # check whether item already exists
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                return Code.FAIL_ITEM_ALREADY_EXISTS
        # insert item into list
        self.item_list.append(Item(name, price, unit))
        return Code.SUCCESS

    def delete_item(self, name: str) -> int:
        """ delete selected item from the item list
        :param name: name of selected item to delete
        :return: running result status code
        """
        # check whether selected item exists
        # if exists, delete item from list
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                self.item_list.pop(i)
                return Code.SUCCESS
        # item not found
        return Code.FAIL_ITEM_NOT_FOUND

    def modify_item(self, name: str, price: float) -> int:
        """ modify the price of selected item in the item list
        :param name: name of selected item to modify
        :param price: new item price
        :return: running result status code
        """
        # check whether selected item exists
        # if exists, modify the price
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                self.item_list[i].price = price
                return Code.SUCCESS
        # item not found
        return Code.FAIL_ITEM_NOT_FOUND

    def clear_item(self) -> int:
        """ clear the item list
        :return: running result status code
        """
        self.item_list.clear()
        return Code.SUCCESS

    def print_user_list(self):
        """ print the user list
        """
        # create table with PrettyTable
        table = pt.PrettyTable()
        table.field_names = ['Username', 'Password', 'Shopping Number', 'Shopping Total']
        # add users into the table as rows
        for i in range(len(self.user_list)):
            table.add_row([
                # Username
                self.user_list[i].username,
                # Password
                self.user_list[i].password,
                # Shopping Number
                len(self.user_list[i].shopping_list),
                # Shopping Total
                self.user_list[i].calculate_sum(),
            ])
        # print the table
        print(table)

    def print_item_list(self):
        """ print the item list
        """
        # create table with PrettyTable
        table = pt.PrettyTable()
        table.field_names = ['Name', 'Price']
        # add items into the table as rows
        for i in range(len(self.item_list)):
            table.add_row([
                # Name
                self.item_list[i].name,
                # Price
                str(self.item_list[i].price) + ' / ' + self.item_list[i].unit,
            ])
        # print the table
        print(table)


####################
# Program Entrance #
####################
if __name__ == '__main__':
    manager = Manager('', '')
    manager.run()
