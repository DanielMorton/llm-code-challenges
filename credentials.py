import getpass


def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return username, password
