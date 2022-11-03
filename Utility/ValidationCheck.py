import re
import string


def username_valid(username: string) -> bool:
    return re.match("[0-9A-Za-z]{4,20}", username) is not None


def username_group_valid(username: string) -> bool:
    return re.match("[0-9A-Za-z;]{4,20}", username) is not None


def password_valid(password: string) -> bool:
    return re.match("(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{7,20}", password) is not None
