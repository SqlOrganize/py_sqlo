"""
Constantes generales.
Se redefinen en funcion del motor de base de datos y otras caracteristicas.
"""
UNDEFINED = "~" #valor no definido
DEFAULT_VALUE = "^" #debe asignarse valor por defecto
EQUAL = "=" #comparacion estrictamente igual
APPROX = "=~" #comparacion aproximadamente igual
APPROX_LEFT = "-=~" #comparacion aproximadamente igual por izquierda (para strings, equivale a LIKE '%something')
APPROX_RIGHT = "=~-" #comparacion aproximadamente igual por derecha (para strings, equivale a LIKE 'something%')
NONEQUAL = "!=" #comparacion distinto
LESS = "<" #comparacion menor
LESS_EQUAL = "<=" #comparacion menor o igual
GREATER = ">" #comparacion mayor
GREATER_EQUAL = ">=" #comparacion mayor o igual
FF = "°°" #prefijo que indica field (utilizado ocasionalmente para definir un valor como field)
OR_ = "OR" #prefijo que indica field (utilizado para indicar concatenacion OR en condiciones)
AND_ = "AND" #prefijo que indica field (utilizado para indicar concatenacion AND en condiciones)

"""
# Ejemplo
container.query("entity").cond(["field", EQUAL, "value"]) #se traduce a field = 'value'
container.query("entity").cond(["field", LESS_EQUAL, 123]) #se traduce a field <= 123
container.query("entity").cond(["field", EQUAL, FF."field2"]) #se traduce a field = field2
container.query("entity").cond([
 *   [
 *      ["field", EQUAL, FF."field2"],
 *      ["field", EQUAL, FF."field3 = OR_]
 *   ], 
 *   ["field", APPROX, "value", AND_] //no es necesario agregar AND_ ya que es el valor por defecto
 * ]) #se traduce a (((field = field2) OR (field = field3)) AND (field LIKE '%VALUE%))

# Operaciones Matematicas
No se definen condiciones para las operaciones matematicas.
El sistema asume que si utilizas una operacion, existe una probabilidad de que la vuelvas a usar en otro lado,
por lo tanto debe definirse un nuevo metodo mapping con la operacion.

# TODO 
Analizar bien como mappear los fields y redefinir el ejemplo a continuacion

SomeEntityMapping {
  def some_new_field(self):
    self.mapping("field1") . " - " . self.mapping("field1")
"""