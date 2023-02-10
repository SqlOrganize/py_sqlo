def add_prefix_recursive(condition=None, prefix:str=None):
    if (condition):
        if (isinstance(condition[0],list)):
            for i, v in enumerate(condition):
                v = add_prefix_recursive(v, prefix)
                condition[i] = v

        else:
            condition[0] = prefix + condition[0]

    return condition
