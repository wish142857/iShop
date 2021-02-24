####################
# [iShop]  ver 1.0 #
####################
import json
import prettytable as pt


class Code:
    """
    Class: Running Result Status Code
    """
    # Succeeded
    SUCCESS = 0
    # Failed: wrong username or password
    FAIL_WRONG_USERNAME_OR_PASSWORD = 1
    # Failed: item not found
    FAIL_ITEM_NOT_FOUND = 2
    # Failed: user already exists
    FAIL_USER_ALREADY_EXISTS = 3
    # Failed: item already exists
    FAIL_ITEM_ALREADY_EXISTS = 3
    # Failed: illegal username or password
    FAIL_ILLEGAL_USERNAME_OR_PASSWORD = 4
    # Failed: illegal item number
    FAIL_ILLEGAL_NUMBER = 5
    # Failed: illegal item price
    FAIL_ILLEGAL_PRICE = 6


class Item:
    """
    Class: Item
    """
    def __init__(self, name: str, price: float, unit: str):
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
    def __init__(self, username: str, password: str, shopping_list=None):
        """
        :param username: username of the user
        :param password: password of the user
        :param shopping_list: shopping list of the user
        """
        self.username = username
        self.password = password
        if shopping_list:
            self.shopping_list = shopping_list
        else:
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
                    # failed: item already exists
                    return Code.FAIL_ITEM_ALREADY_EXISTS
            # succeed: insert item into list
            self.shopping_list.append({'item': item, 'number': number})
            return Code.SUCCESS
        elif not item:
            # failed: item not found
            return Code.FAIL_ITEM_NOT_FOUND
        else:
            # failed: illegal number
            return Code.FAIL_ILLEGAL_NUMBER

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
                    # succeed: delete item from list
                    self.shopping_list.pop(i)
                    return Code.SUCCESS
            # failed: item not found
            return Code.FAIL_ITEM_NOT_FOUND
        else:
            return Code.FAIL_ITEM_NOT_FOUND

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
                    # succeed: modify the number
                    self.shopping_list[i]['number'] = number
                    return Code.SUCCESS
            # failed: item not found
            return Code.FAIL_ITEM_NOT_FOUND
        elif not item:
            # failed: item not found
            return Code.FAIL_ITEM_NOT_FOUND
        else:
            # failed: illegal number
            return Code.FAIL_ILLEGAL_NUMBER

    def clear_item(self) -> int:
        """ clear the shopping list
        :return: running result status code
        """
        # succeed: clear the shopping list
        self.shopping_list.clear()
        return Code.SUCCESS

    def print_shopping_list(self):
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
    DATA_FILE_PATH = 'data.txt'
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
        print('********** iShop **********')
        self.current_status = Manager.USER_OFFLINE_STATUS
        self.load()
        # ***** Loop *****
        ongoing = True
        while ongoing:
            if self.current_status == Manager.USER_OFFLINE_STATUS:
                # *** Handle User Offline ***
                self.help()  # print hint for user
                while True:
                    user_input = input('\n(?) >>>')
                    if user_input == 'logon':
                        # * get input *
                        username = input('* Please input username:')
                        password = input('* Please input password:')
                        # * perform operation *
                        result = self.logon(username, password)
                        # * check result *
                        if result == Code.FAIL_ILLEGAL_USERNAME_OR_PASSWORD:
                            print('* [Failed] Illegal username or password!')
                        elif result == Code.FAIL_USER_ALREADY_EXISTS:
                            print('* [Failed] User already exists!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] Registered (' + username + ') successfully.')
                    elif user_input == 'login':
                        # * get input *
                        username = input('* Please input username:')
                        password = input('* Please input password:')
                        # * perform operation *
                        result = self.login(username, password)
                        # * check result *
                        if result == Code.FAIL_WRONG_USERNAME_OR_PASSWORD:
                            print('* [Failed] Wrong username or password!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] Login (' + username + ') successfully.')
                            break
                    elif user_input == 'help':
                        # * perform operation *
                        self.help()  # print hint for user
                    elif user_input == 'exit':
                        # * perform operation *
                        ongoing = False  # label to exit outer loop
                        break
                    else:
                        print('* [Failed] Unknown command!')
            elif self.current_status == Manager.USER_ONLINE_STATUS:
                # *** Handle User Online ***
                self.help()  # print hint for user
                while True:
                    user_input = input('\n(' + self.current_user.username + ') >>>')
                    if user_input == 'shop':
                        # * perform operation *
                        self.print_item_list()
                    elif user_input == 'cart':
                        # * perform operation *
                        self.current_user.print_shopping_list()
                    elif user_input == 'insert':
                        # * get input *
                        self.print_item_list()  # print the item list
                        item_name = input('* Please input item name:')
                        number = input('* Please input number:')
                        # * perform operation *
                        try:
                            number = float(number)
                        except ValueError:
                            print('* [Failed] illegal number!')
                            continue
                        result = self.current_user.insert_item(self.search_item(item_name), number)
                        # * check result *
                        if result == Code.FAIL_ITEM_ALREADY_EXISTS:
                            print('* [Failed] item already exists!')
                        elif result == Code.FAIL_ITEM_NOT_FOUND:
                            print('* [Failed] item not found!')
                        elif result == Code.FAIL_ILLEGAL_NUMBER:
                            print('* [Failed] illegal number!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] insert item successfully.')
                            self.current_user.print_shopping_list()  # print the shopping list
                    elif user_input == 'delete':
                        # * get input *
                        self.print_item_list()  # print the item list
                        item_name = input('* Please input item name:')
                        # * perform operation *
                        result = self.current_user.delete_item(self.search_item(item_name))
                        # * check result *
                        if result == Code.FAIL_ITEM_NOT_FOUND:
                            print('* [Failed] item not found!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] delete item successfully.')
                            self.current_user.print_shopping_list()  # print the shopping list
                    elif user_input == 'modify':
                        # * get input *
                        self.current_user.print_shopping_list()  # print the shopping list
                        item_name = input('* Please input item name:')
                        number = input('* Please input number:')
                        # * perform operation *
                        try:
                            number = float(number)
                        except ValueError:
                            print('* [Failed] illegal number!')
                            continue
                        result = self.current_user.modify_item(self.search_item(item_name), number)
                        # * check result *
                        if result == Code.FAIL_ITEM_NOT_FOUND:
                            print('* [Failed] item not found!')
                        elif result == Code.FAIL_ILLEGAL_NUMBER:
                            print('* [Failed] illegal number!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] modify item successfully.')
                            self.current_user.print_shopping_list()  # print the shopping list
                    elif user_input == 'pay':
                        # * perform operation *
                        self.current_user.print_shopping_list()  # print the shopping list
                        result = self.current_user.calculate_sum()
                        print('* [Succeed] your bill: ' + str(result) + '.')
                        self.current_user.clear_item()  # clear the shopping list
                        self.current_user.print_shopping_list()  # print the shopping list
                    elif user_input == 'logout':
                        # * perform operation *
                        result = self.logout()
                        # * check result *
                        if result == Code.SUCCESS:
                            print('* [Succeed] Logout successfully.')
                        break
                    elif user_input == 'help':
                        # * perform operation *
                        self.help()  # print hint for user
                    elif user_input == 'exit':
                        # * perform operation *
                        ongoing = False  # label to exit outer loop
                        break
                    else:
                        print('* [Failed] Unknown command!')
            elif self.current_status == Manager.ADMIN_ONLINE_STATUS:
                # *** Handle Admin Online ***
                self.help()  # print hint for user
                while True:
                    user_input = input('\n(Admin) >>>')
                    if user_input == 'user':
                        # * perform operation *
                        self.print_user_list()
                    elif user_input == 'shop':
                        # * perform operation *
                        self.print_item_list()
                    elif user_input == 'insert':
                        # * get input *
                        self.print_item_list()  # print the item list
                        item_name = input('* Please input item name:')
                        price = input('* Please input price:')
                        unit = input('* Please input unit:')
                        # * perform operation *
                        try:
                            price = float(price)
                        except ValueError:
                            print('* [Failed] illegal number!')
                            continue
                        result = self.insert_item(item_name, price, unit)
                        # * check result *
                        if result == Code.FAIL_ILLEGAL_PRICE:
                            print('* [Failed] illegal item price!')
                        elif result == Code.FAIL_ITEM_ALREADY_EXISTS:
                            print('* [Failed] item already exists!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] insert item successfully.')
                            self.print_item_list()  # print the item list
                    elif user_input == 'delete':
                        # * get input *
                        self.print_item_list()  # print the item list
                        item_name = input('* Please input item name:')
                        # * perform operation *
                        result = self.delete_item(item_name)
                        # * check result *
                        if result == Code.FAIL_ITEM_NOT_FOUND:
                            print('* [Failed] item not found!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] delete item successfully.')
                            self.print_item_list()  # print the item list
                    elif user_input == 'modify':
                        # * get input *
                        self.print_item_list()  # print the item list
                        item_name = input('* Please input item name:')
                        price = input('* Please input price:')
                        # * perform operation *
                        try:
                            price = float(price)
                        except ValueError:
                            print('* [Failed] illegal number!')
                            continue
                        result = self.modify_item(item_name, price)
                        # * check result *
                        if result == Code.FAIL_ILLEGAL_PRICE:
                            print('* [Failed] illegal item price!')
                        elif result == Code.FAIL_ITEM_NOT_FOUND:
                            print('* [Failed] item not found!')
                        elif result == Code.SUCCESS:
                            print('* [Succeed] modify item successfully.')
                            self.print_item_list()  # print the item list
                    elif user_input == 'clear':
                        # * perform operation *
                        result = self.clear_item()
                        # * check result *
                        if result == Code.SUCCESS:
                            print('* [Succeed] Clear item list successfully.')
                            self.print_item_list()  # print the item list
                    elif user_input == 'logout':
                        # * perform operation *
                        result = self.logout()
                        # * check result *
                        if result == Code.SUCCESS:
                            print('* [Succeed] Logout successfully.')
                        break
                    elif user_input == 'help':
                        # * perform operation *
                        self.help()  # print hint for user
                    elif user_input == 'exit':
                        # * perform operation *
                        ongoing = False  # label to exit outer loop
                        break
                    else:
                        print('* [Failed] Unlknown command!')
        # ***** Save *****
        self.save()
        print('* [Succeed] Program exit successfully.')

    def help(self):
        """ print hint for user
        """
        if self.current_status == Manager.USER_OFFLINE_STATUS:
            # print hint for user not logged in
            print('\n****** User Offline ******')
            print('<logon>:  user register')
            print('<login>:  user login')
            print('<help>:   display hint')
            print('<exit>:   exit program')
            print('*************************')
        elif self.current_status == Manager.USER_ONLINE_STATUS:
            # print hint for user logged in
            print('\n****** User  Online ******')
            print('<shop>:   display item list')
            print('<cart>:   display shopping cart')
            print('<insert>: insert items')
            print('<delete>: delete items')
            print('<modify>: modify items')
            print('<pay>:    pay the bill')
            print('<logout>: user logout')
            print('<help>:   print hint')
            print('<exit>:   exit program')
            print('*************************')
        elif self.current_status == Manager.ADMIN_ONLINE_STATUS:
            # print hint for admin logged in
            print('\n****** Admin Online *****')
            print('<user>:   display user list')
            print('<shop>:   display item list')
            print('<insert>: insert items')
            print('<delete>: delete items')
            print('<modify>: modify items')
            print('<clear>:  clear items')
            print('<logout>: user logout')
            print('<help>:   display hint')
            print('<exit>:   exit program')
            print('************************A*')

    def load(self):
        try:
            file = open(Manager.DATA_FILE_PATH, 'r+')
            item_list_string = file.readline()
            user_list_string = file.readline()
            self.item_list = [Item(item['name'], item['price'], item['unit']) for item in json.loads(item_list_string)]  # convert to object
            self.user_list = [
                User(user['username'], user['password'], [{'item': Item(pair['item']['name'], pair['item']['price'], pair['item']['unit']), 'number': pair['number']} for pair in user['shopping_list']])
                for user in json.loads(user_list_string)
            ]  # convert to object
            file.close()
            print('* [Succeed] Load data from <' + Manager.DATA_FILE_PATH + '> successfully.')
        except FileNotFoundError:
            print('* [Failed] Load data from <' + Manager.DATA_FILE_PATH + '> failed.')

    def save(self):
        file = open('data.txt', 'w')
        item_list_string = json.dumps([{'name': item.name, 'price': item.price, 'unit': item.unit} for item in self.item_list])  # convert to string
        user_list_string = json.dumps([
            {'username': user.username,
             'password': user.password,
             'shopping_list': [{'item': {'name': pair['item'].name, 'price': pair['item'].price, 'unit': pair['item'].unit}, 'number': pair['number']} for pair in user.shopping_list]
             }
            for user in self.user_list
        ])  # convert to string
        file.write(item_list_string + '\n')
        file.write(user_list_string + '\n')
        file.close()
        print('* [Succeed] Save data into <' + Manager.DATA_FILE_PATH + '> successfully.')

    def logon(self, username: str, password: str) -> int:
        """
        :param username: username of the user
        :param password: password of the user
        :return: running result status code
        """
        # check whether arguments are valid
        if not username or not password:
            # failed: illegal username or password
            return Code.FAIL_ILLEGAL_USERNAME_OR_PASSWORD
        # check whether user already exists
        if self.admin_username == username:
            # failed: user already exists
            return Code.FAIL_USER_ALREADY_EXISTS
        for i in range(len(self.user_list)):
            if self.user_list[i].username == username:
                # failed: user already exists
                return Code.FAIL_USER_ALREADY_EXISTS
        # succeed: user logon
        self.user_list.append(User(username, password))
        return Code.SUCCESS

    def login(self, username: str, password: str) -> int:
        """
        :param username: username of the user
        :param password: password of the user
        :return: running result status code
        """
        # check whether is admin
        if self.admin_username == username and self.admin_password == password:
            # succeed: admin login
            self.current_user = None
            self.current_status = Manager.ADMIN_ONLINE_STATUS
            return Code.SUCCESS
        # check whether user exists
        for i in range(len(self.user_list)):
            if self.user_list[i].username == username and self.user_list[i].password == password:
                # succeed: user login
                self.current_user = self.user_list[i]
                self.current_status = Manager.USER_ONLINE_STATUS
                return Code.SUCCESS
        # failed: wrong username or password
        return Code.FAIL_WRONG_USERNAME_OR_PASSWORD

    def logout(self) -> int:
        """
        :return: running result status code
        """
        self.current_user = None
        self.current_status = Manager.USER_OFFLINE_STATUS
        return Code.SUCCESS

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
        # check whether price is valid
        if price < 0:
            # failed: illegal item price
            return Code.FAIL_ILLEGAL_PRICE
        # check whether item already exists
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                # failed: item already exists
                return Code.FAIL_ITEM_ALREADY_EXISTS
        # succeed: insert item into list
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
                # succeed: delete item from list
                self.item_list.pop(i)
                return Code.SUCCESS
        # failed: item not found
        return Code.FAIL_ITEM_NOT_FOUND

    def modify_item(self, name: str, price: float) -> int:
        """ modify the price of selected item in the item list
        :param name: name of selected item to modify
        :param price: new item price
        :return: running result status code
        """
        # check whether price is valid
        if price < 0:
            # failed: illegal item price
            return Code.FAIL_ILLEGAL_PRICE
        # check whether selected item exists
        # if exists, modify the price
        for i in range(len(self.item_list)):
            if self.item_list[i].name == name:
                # succeed: modify the price
                self.item_list[i].price = price
                return Code.SUCCESS
        # failed: item not found
        return Code.FAIL_ITEM_NOT_FOUND

    def clear_item(self) -> int:
        """ clear the item list
        :return: running result status code
        """
        # succeed: clear the item list
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
    manager = Manager('NUS', 'NUS')
    manager.run()
