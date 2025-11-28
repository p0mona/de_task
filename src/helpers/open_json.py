import json


def open_json(path: str) -> any:
    """
    Open JSON file

    Args:
        path(str): path to JSON file
    """

    with open(path, "r", encoding="utf-8") as file:
        file = json.load(file)
    return file
