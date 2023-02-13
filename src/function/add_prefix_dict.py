def add_prefix_dict(d:dict, prefix:str=""):
    return {prefix + str(key): val for key, val in d.items()}
