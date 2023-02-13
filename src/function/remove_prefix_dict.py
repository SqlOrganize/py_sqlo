def remove_prefix_dict(d:dict, prefix:str=""):
    return {str(key).removeprefix(prefix): val for key, val in d.items()}
