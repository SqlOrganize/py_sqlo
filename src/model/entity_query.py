
from src.config import AND_, EQUAL, OR_
from src.function.add_prefix_multi_list import add_prefix_multi_list
from src.function.add_prefix_dict import add_prefix_dict
from src.function.remove_prefix_multi_list import remove_prefix_multi_list
from src.function.remove_prefix_dict import remove_prefix_dict

from src.icontainer import IContainer

class EntityQuery:
    container: IContainer

    def __init__(self, entity_name) -> None:
        self._entity_name = entity_name
        self._condition = []
        """
        condicion
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """
        
        self._order = {}
        self._page = 1
        self._size = 100
        self._fields = []
        """
        Deben estar definidos en el mapping field, se realizará la traducción 
        correspondiente
        . indica aplicacion de funcion de agregacion
        - indica que pertenece a una relacion
        Ej ["nombres", "horas_catedra.sum", "edad.avg", "com_cur-horas_catedra]
        """
        self._fields_concat = {}
        """
        Similar a _fields pero se define un alias para concatenar un conjunto de fields
        Ej ["nombre" => ["nombres", "apellidos"], "max" => ["horas_catedra.max", "edad.max"]]
        """
        self._group = []      
        """
        Similar a fields pero campo de agrupamiento
        """
        self._group_concat = {}      
        """
        Similar a _fields_concat pero campo de agrupamiento
        """
        self._having = []
        """
        condicion de agrupamiento
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """

    def cond (self, condition:list):
        self._condition.append(condition)
        return self

    def param (self, key:str, value): 
        return self.cond([key, "=",value])


    def params (self, params:dict):
        for k,v in params.items():
            self.cond([k,"=",v])
        return self

    def order (self, order:dict):
        self._order = order
        return self
    
    def size(self, size):
        self._size = size
        return self
    
    def page(self, page):
        self._page = page
        return self

    def field(self, field: str):
        self._fields.append(field)
        return self

    def fields(self, fields: list[str]):
        if not fields:
            return self.fields_tree()
        
        self._fields = list(set(self._fields + fields))
        return self

    def fields_tree(self):
        self._fields = EntityQuery.container.tools(self._entity_name).field_names()
        return self

    def fields_concat(self, fields: dict[list[str]]):
        self._fields_concat.update(fields)
        return self

    def group(self, group: list[str]):
        self._group = list(set(self._group + group))
        return self

    def group_concat(self, group: dict[list[str]]):
        self._group_concat.update(group)
        return self

    def having(self, having: list):
        self._having.append(having)
        return self

    def entity_name(self, entity_name: str):
        self._entity_name = entity_name
        return self

    def _add_prefix(self, prefix: str):
        self._condition = add_prefix_multi_list(self._condition, prefix)
        self._order = add_prefix_dict(self._order, prefix)
        return self

    def _remove_prefix(self, prefix: str):
        self._condition = remove_prefix_multi_list(self._condition, prefix)
        self._order = remove_prefix_dict(self._order, prefix)
        return self

    def unique(self, params:dict):
        """ definir condicion para campos unicos 
        # ejemplo params
        {"field_name":"field_value", ...}
        
        # campos unicos simples
        Se definen a traves del atributo Entity._unique

        # campos unicos multiples
        Se definen a traves del atributo Entity._unique_multiple
        """
        unique_fields: list = EntityQuery.container.entity(self._entity_name).unique()
        unique_fields_multiple: list = EntityQuery.container.entity(self._entity_name).unique_multiple()
        
        condition = []
        # if "id" in params and params["id"]:
        #     condition.append(["id", EQUAL, params["id"]])

        first = True 
        
        for f in unique_fields:
            for k, v in params.items():
                if k == f and v:
                    if first:
                        con = AND_
                        first = False
                    else:
                        con = OR_    

                    condition.append([k, EQUAL, v, con])
        
        if unique_fields_multiple:
            condition_multiple = []
            first = True 
            exists_condition_multiple = True #si algun campo de la condicion multiple no se encuentra definido, se carga en True.
            for f in unique_fields_multiple:
                if not exists_condition_multiple:
                    break

                exists_condition_multiple = False

                for k, v in params.items():
                    if k == f:
                        exists_condition_multiple = True
                        if first and condition:
                            con = OR_
                            first = False
                        else:
                            con = AND_    

                        condition_multiple.append([k, EQUAL, v, con])

            if exists_condition_multiple and condition_multiple:
                condition.append(condition_multiple)

        if not condition:
            raise "Error al definir condition unica"

        self.cond(condition)

        return self

    def _sql_fields(self) -> str:
        """
        SQL FIELDS
        """
        field_names = list(set(self._group + self._fields))
        sql_fields = []

        for field_name in field_names:
            ff = EntityQuery.container.explode_field(self.entity_name, field_name)
            map = EntityQuery.container.mapping(ff["entity_name"], ff["field_id"]).map(ff["field_name"])
            $prefix = (!empty($f["field_id"])) ? $f["field_id"] . "-" : "";
            $alias = (is_integer($key)) ? $prefix . $f["field_name"] : $key;
            $f = $map . " AS \"" . $alias . "\"";

            



    $fieldsQuery_ = [];
    foreach($fields as $key => $field_name){
      if(is_array($field_name)){
        if(is_integer($key)) throw new Exception("Debe definirse un alias para la concatenacion (key must be string)");
        $map_ = [];
        foreach($field_name as $fn){
          $f = $this->container->explode_field($this->entity_name, $fn);
          $m = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
          array_push($map_, $m);
        } 
        $f = "CONCAT_WS(', ', " . implode(",",$map_) . ") AS " . $key;
      } else {
        $f = $this->container->explode_field($this->entity_name, $field_name);
        $map = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
        $prefix = (!empty($f["field_id"])) ? $f["field_id"] . "-" : "";
        $alias = (is_integer($key)) ? $prefix . $f["field_name"] : $key;
        $f = $map . " AS \"" . $alias . "\"";
      }
      array_push($fieldsQuery_, $f);
    }

    return implode(', 
', $fieldsQuery_);
  }



    def sql() -> str:
        """
        Definir SQL
        """
        
        
        """
    $fieldsQuery = $this->fieldsQuery();
    $group = $this->groupBy();
    $having = $this->condition($this->having);    
    $condition = $this->condition($this->condition);
    $order = $this->_order();
    $sql = "SELECT DISTINCT
{$fieldsQuery}
{$this->from()}
{$this->join()}
" . concat($condition, 'WHERE ') . "
{$group}
" . concat($having, 'HAVING ') . "
{$order}
{$this->limit($this->page, $this->size)}
";

    return $sql;
  }

    def column(number: int = 0) -> list[str]:
        """
        Retornar columna indicada en parametro
        @example container.query("entity").field("_count").column()
        """
        """
    $sql = $this->sql();
    $result = $this->container->db()->query($sql);
    $response = $this->container->db()->fetch_all_columns($result, $number);
    $result->free();
    return $response;
  }

  /**
   * Similar a column pero retorna un valor, error si no existe
   */
  public function columnOne($number = 0){
    /**
     * Retorna la primera columna definidas
     * @example $render->fields(["id"]);
     * @example $render->fields(["_count"]);
     */
    $response = $this->column($number);
    if(count($response) > 1 ) throw new Exception("La consulta retorno mas de un resultado");
    elseif(count($response) == 1) return $response[0];
    else throw new Exception("La consulta no arrojó resultados");
  }

  /**
   * Similar a columnOne, null si no existe
   */
  public function columnOneOrNull($number = 0){
    /**
     * Retorna la primera columna definidas
     * @example $render->fields(["id"]);
     * @example $render->fields(["_count"]);
     */
    $response = $this->column($number);
    if(count($response) > 1 ) throw new Exception("La consulta retorno mas de un resultado");
    elseif(count($response) == 1) return $response[0];
    else return null;
  }

  /**
   * ejecucion del sql sin control adicional
   */
  public function all(){
    $sql = $this->sql();
    $result = $this->container->db()->query($sql);
    $rows = $result->fetch_all(MYSQLI_ASSOC);
    $result->free();
    return $rows;    
  }

  /**
   * retornar el primer elemento de la consulta, error si la consulta no retorna elementos
   */
  public function first(){
    $sql = $this->sql();
    $result = $this->container->db()->query($sql);
    $rows = $result->fetch_all(MYSQLI_ASSOC);
    $result->free();
    if(empty($rows)) throw new Exception("La consulta no arrojó resultados");
    return $rows[0];    
  }

  /**
   * retornar el primer elemento de la consulta, null si la consulta no retorna elementos
   */
  public function firstOrNull(){
    $sql = $this->sql();
    $result = $this->container->db()->query($sql);
    $rows = $result->fetch_all(MYSQLI_ASSOC);
    $result->free();
    if(empty($rows)) return null;
    return $rows[0];    
  }

  /**
   * consulta de un valor
   * error si la cantidad de elementos a retornar es distinto de 1
   */
  public function one(){
    $response = $this->all();
    if(count($response) > 1 ) throw new Exception("La consulta retorno mas de un resultado");
    elseif(count($response) == 1) return $response[0];
    else throw new Exception("La consulta no arrojó resultados");
  }

   /**
   * consulta de un valor
   * error si la cantidad de elementos es mayor a 1
   * null si la cantidad de elementos a retorar es 0
   */
  public function oneOrNull(){
    $response = $this->all();
    if(count($response) > 1 ) throw new Exception("La consulta retorno mas de un resultado");
    elseif(count($response) == 1) return $response[0];
    else return null;
  }



  protected function mapping($field_name){
     /**
     * Interpretar prefijo y obtener mapping
     */
    $f = $this->container->explode_field($this->entity_name, $field_name);
    $m = $this->container->mapping($f["entity_name"], $f["field_id"]);
    return [$m, $f["field_name"]];
  }

  
  protected function groupBy(){
    $group_ = [];
    foreach($this->group as $key => $field_name){
      if(is_array($field_name)){
        if(is_integer($key)) throw new Exception("Debe definirse un alias para la concatenacion (key must be string)");
        $f = $key;
      } else {
        $f = $this->container->explode_field($this->entity_name, $field_name);
        $map = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
      }
      array_push($group_, $map);
    }

    return empty($group_) ? "" : "GROUP BY " . implode(", ", $group_) . "
";
  }

  protected function join(){
    $sql = "";
    $tree = $this->container->tree($this->entity_name);
    $this->joinFk($tree, "", $sql);
    return $sql;
  }

  protected function joinFk(array $tree, $tablePrefix, &$sql){
    if (empty ($tablePrefix)) $tablePrefix = $this->container->entity($this->entity_name)->getAlias();

    foreach ($tree as $prefix => $value) {      
      $entitySn =  $this->container->entity($value["entity_name"])->sn_();
      $sql .= $this->_join($entitySn, $value["field_name"], $tablePrefix, $prefix) . "
";

      if(!empty($value["children"])) $this->joinfk($value["children"], $prefix, $sql);
    }
  }

  protected function limit($page = 1, $size = false){
    if ($size) {
      return " LIMIT {$size} OFFSET " . ( ($page - 1) * $size ) . "
";
    }
    return "";
  }

  protected function from(){    
    return " FROM 

" . $this->container->entity($this->entity_name)->sn_() . "

 AS {$this->container->entity($this->entity_name)->getAlias()}
";
  }

  /**
   * Definir SQL de relacion 
   */
  protected function _join($entitySn, $field, $fromTable, $table){
    return "LEFT OUTER JOIN " . $entitySn . " AS $table ON ($fromTable.$field = $table.id)
";
  }


  protected function condition($condition){
    if(empty($condition)) return "";
    $conditionMode = $this->conditionRecursive($condition);
    return $conditionMode["condition"];
  }

  /**
   * Metodo recursivo para definir condiciones avanzada (considera relaciones)
   * Para facilitar la definicion de condiciones, retorna un array con dos elementos:
   * "condition": SQL
   * "mode": Concatenacion de condiciones "AND" | "OR"
   */
  protected function conditionRecursive(array $condition){
    /**
     * si en la posicion 0 es un string significa que es un campo a buscar, caso contrario es un nuevo conjunto (array) de campos que debe ser recorrido
     */
    if(is_array($condition[0])) return $this->conditionIterable($condition);
    
    $option = (empty($condition[1])) ? "=" : $condition[1]; //por defecto se define "="
    $value = (!isset($condition[2])) ? null : $condition[2]; //hay opciones de configuracion que pueden no definir valores
    /**
     * No usar empty, puede definirse el valor false
     */
    $mode = (empty($condition[3])) ? "AND" : $condition[3];  //el modo indica la concatenacion con la opcion precedente, se usa en un mismo conjunto (array) de opciones

    $condicion = $this->conditionFieldCheckValue($condition[0], $option, $value);
    /**
     * El campo de identificacion del array posicion 0 no debe repetirse en las condiciones no estructuradas y las condiciones estructuras
     * Se recomienda utilizar un sufijo por ejemplo "_" para distinguirlas mas facilmente
     */
    return ["condition" => $condicion, "mode" => $mode];
  }
  
  
   /**
   * metodo de iteracion para definir condiciones
   */
  protected function conditionIterable(array $conditionIterable) { 
    $conditionModes = array();

    for($i = 0; $i < count($conditionIterable); $i++){
      $conditionMode = $this->conditionRecursive($conditionIterable[$i]);
      array_push($conditionModes, $conditionMode);
    }

    $modeReturn = $conditionModes[0]["mode"];
    $condition = "";

    foreach($conditionModes as $cm){
      $mode = $cm["mode"];
      if(!empty($condition)) $condition .= "
" . $mode . " ";
      $condition.= $cm["condition"];
    }

    return ["condition"=>"(
".$condition."
)", "mode"=>$modeReturn];
  }


  /**
   * Combinar parametros y definir SQL con la opcion
   */
  protected function conditionFieldCheckValue($field, $option, $value){    
    if(!is_array($value)) {
      $condition = $this->conditionField($field, $option, $value);
      if(!$condition) throw new Exception("No pudo definirse el SQL de la condicion del campo: {$this->entity_name}.{$field}");
      return $condition;
    }

    $condition = "";
    $cond = false;

    foreach($value as $v){
      if($cond) {
        if($option == "=") $condition .= " OR ";
        elseif($option == "!=") $condition .= " AND ";
        else throw new Exception("Error al definir opción");
      } else $cond = true;

      $condition_ = $this->conditionFieldCheckValue($field, $option, $v);
      $condition .= $condition_;
    }

    return "(
  ".$condition."
)";
  }

  /**
   * Traducir campo y definir SQL con la opcion
   */
  protected function conditionField($field, $option, $value){
    $f = $this->container->explode_field($this->entity_name, $field);

    if(strpos($value, FF) === 0) { //definir condicion entre fields
      $v = $this->container->explode_field($this->entity_name, substr($value, strlen(FF)));
      $fieldSql1 = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
      $fieldSql2 = $this->container->mapping($v["entity_name"], $v["field_id"])->_($v["field_name"]);
      
      switch($option) {
        case "=~": return "(lower(CAST({$fieldSql1} AS CHAR)) LIKE CONCAT('%', lower(CAST({$fieldSql2} AS CHAR)), '%'))";
        case "!=~": return "(lower(CAST({$fieldSql1} AS CHAR)) NOT LIKE CONCAT('%', lower(CAST({$fieldSql2} AS CHAR)), '%'))";
        default: return "({$fieldSql1} {$option} {$fieldSql2}) ";  
      }
    }

    return $this->container->condition($f["entity_name"], $f["field_id"])->_($f["field_name"], $option, $value);
    /**
     * Debido a la complejidad del metodo "condition" se proporciona un ejemplo para entender su comportamiento: 
     * Desde la entidad alumno, Se quiere traducir "persona-numero_documento.max"
     * Se define una instancia de condition con los siguientes atributos: 
     *    entity_name = "persona"
     *    prefix = "persona-"
     * 
     * Desde condition se ejecuta
     * 1) _("numero_documento.max", "=", "something") //verifica si hay metodo local "numeroDocumentoMax" sino invoca a _defineCondition("numero_documento.max")}
     * 2) _defineCondition("numero_documento.max") //traduce la funcion necesaria para armar la condicion, en este caso  se traduce como "_string"
     * 3) _string("numero_documento.max", "=", "something") //define el mapeo del field y el valor
     *    Para el mapeo, utiliza  $field = $this->container->mapping("persona", "persona-")->_("numero_documento.max"); que se traduce a MAX(persona-numero_documento)
     *    Para el valor, utiliza $this->container->value("persona", "persona-")->_set("numero_documento.max","something")... value->_check("numero_documento.max") ...value->_sql("numero_documento.max") que se traduce a "'something'"
     */

  }



  /**
   * Procesar atributo order y definir ordenamiento
   */
  protected function _order(){
    $entity = $this->container->entity($this->entity_name);
    $orderDefault = (!empty($entity->getOrderDefault())) ? $entity->getOrderDefault() : array_fill_keys($entity->main, "asc"); //se retorna ordenamiento por defecto considerando campos principales nf de la entidad principal

    foreach($this->order as $key => $value) {
      if(array_key_exists($key, $orderDefault)) unset($orderDefault[$key]);
    }

    $order = array_merge($this->order, $orderDefault);
    
    $sql = '';
    foreach($order as $key => $value){
      $value = ((strtolower($value) == "asc") || ($value === true)) ? "asc" : "desc";
      $f = $this->container->explode_field($this->entity_name, $key);
      $map_ = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
      $sql_ = "{$map_} IS NULL, {$map_} {$value}";
      $sql .= concat($sql_, ', ', ' ORDER BY', $sql);
    }
    return $sql;
  }
}

"""