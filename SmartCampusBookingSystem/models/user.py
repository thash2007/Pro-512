class User:

    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role