
def snake_case_to_camel_case(snake_str:str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components[0:])