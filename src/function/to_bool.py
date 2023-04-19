

def to_bool(param: any):
    if isinstance(param, str):
        return param.lower()[0] in ['t', '1', 'v', 'y', 's', 'o'] #valido para variantes de true, verdadero, yes, si, ok

    return param in [True, 1] 