def concat(value: str, connect_no_empty: str, connect_empty: str = None, connect_cond: any = None) -> str:
    """
    Concatenar valores en funcion de ciertas condiciones
    """
    if not value:
        return ''

    connect = (connect_no_empty if connect_cond else connect_empty) if connect_empty else connect_no_empty    
    
    return connect + " " + value