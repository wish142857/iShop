class Code:
    """
    Class: Running Result Status Code
    """
    SUCCESS = 0


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
        if item and number > 0:
            self.shopping_list.append({'item': item, 'number': number})
            return Code.SUCCESS

        return False

    def delete_item(self, item: Item) -> bool:
        """ delete selected item from the shopping list
        :param item:
        :return:
        """
        if item:
            for i in range(len(self.shopping_list)):
                if self.shopping_list[i]['item'] == item:
                    self.shopping_list.pop(i)
                    return True
        return False

    def modify_item(self, item: Item, number: float) -> bool:
        if item and number > 0:
            for i in range(len(self.shopping_list)):
                if self.shopping_list[i]['item'] == item:
                    self.shopping_list[i]['number'] = number
                    return True
        return False

    def clear_item(self) -> bool:
        """ clear shopping list
        :return: whether running successfully
        """
        self.shopping_list.clear()
        return True

    def calculate_sum(self) -> float:
        """ calculate the sum of items in the shopping list
        :return: sum of items in the shopping list
        """
        item_sum = 0.0
        for i in range(len(self.shopping_list)):
            item_sum += self.shopping_list[i]['item'].price * self.shopping_list[i]['number']
        return item_sum


class Manager:
    """
    Class: Program Manager
    """
    USER_OFFLINE_STATUS = 0     # status code when user not logged in
    USER_ONLINE_STATUS = 1      # status code when user logged in
    ADMIN_ONLINE_STATUS = 2     # status code when admin logged in

    def __init__(self, username: str, password: str = ''):
        """
        :param username: username of the admin
        :param password: password of the admin
        """
        self.admin_username = username
        self.admin_password = password
        self.current_user = None
        self.current_status = Manager.USER_OFFLINE_STATUS
        self.item_list = []
        self.user_list = []


    def run(self):
        while True:
            print('Hello, world')

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

    def print_hint(self):
        """ print hint for user
        """
        if self.current_status == Manager.USER_OFFLINE_STATUS:
            # print hint for user not logged in
            print('<logon>')
            print('<login>')
            print('<logout>')
            print('<help>')
            print('<exit>')
        elif self.current_status == Manager.USER_ONLINE_STATUS:
            # print hint for user logged in
            print('<logon>')
            print('<login>')
            print('<logout>')
            print('<help>')
            print('<exit>')
        elif self.current_status == Manager.ADMIN_ONLINE_STATUS:
            # print hint for admin logged in
            print('<logon>')
            print('<login>')
            print('<logout>')
            print('<help>')
            print('<exit>')

    def insert_item(self):
        pass

    def delete_item(self):
        pass

    def modify_item(self):
        pass

    def display_item(self):
        pass


if __name__ == '__main__':
    manager = Manager()
    manager.run()

