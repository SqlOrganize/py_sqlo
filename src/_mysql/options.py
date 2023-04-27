
OPTIONS = {
    "EQUAL":"=", #comparacion estrictamente igual
    "NONEQUAL":"!=", #comparacion distinto
    "UNDEFINED":"~", #valor no definido
    "DEFAULT":"DEFAULT", #debe asignarse valor por defecto
    "APPROX":"APPROX", #comparacion aproximadamente igual
    "APPROX_LEFT":"-=~", #comparacion aproximadamente igual por izquierda (para strings, equivale a LIKE '%something')
    "APPROX_RIGHT":"=~-", #comparacion aproximadamente igual por derecha (para strings, equivale a LIKE 'something%')
    "NONAPPROX":"NONAPPROX", #comparacion apriximadamente distinto
    "AND":"AND", "AND"
    "OR":"OR", "OR"
    "$":"$", #prefijo que indica field (utilizado para indicar concatenacion AND en condiciones)
    "LESS":"<", #comparacion menor
    "LESS_EQUAL":"<=", #comparacion menor o igual
    "GREATER":">", #comparacion mayor
    "GREATER_EQUAL":">=" #comparacion mayor o igual
}
