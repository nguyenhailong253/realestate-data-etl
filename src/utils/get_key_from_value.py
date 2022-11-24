def get_key_from_value(dictionary: dict, value: str) -> str:
    for key, val in dictionary.items():
        if val == value:
            return key
    return None
