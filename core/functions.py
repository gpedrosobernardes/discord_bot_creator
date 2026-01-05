import re
from datetime import datetime


def has_number(string: str) -> bool:
    return any(char.isnumeric() for char in string)


def has_symbols(string: str) -> bool:
    return bool(re.search(r"[-!$%^&*()_+|~=`{}\[\]:\";'<>?,./\\´§¨#@ªº°]", string))


def get_time(string: str):
    return datetime.now().strftime(string)
