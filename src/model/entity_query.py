

from icontainer import IContainer

class EntityQuery:
    container: IContainer

    def __init__(self, entityName) -> None:
        self._entityName = entityName
        self._condition = []
        """
        condicion
        array multiple cuya raiz es [field,option,value], ejemplo: [["nombre","=","unNombre"],[["apellido","=","unApellido"],["apellido","=","otroApellido","OR"]]]
        """
        
        self._order = []
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

        self._group = []      
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

    def fields(self, fields: list):
        if not fields:
            return self.fieldsTree()
        
        self._fields = list(set(self._fields + fields))
        return self

    def fieldsTree(self):
        self._fields = EntityQuery.container.tools(self._entityName).fieldNames()
        return self

    def group(self, group: list):
        self._group = list(set(self._group + group))
        return self

    def having(self, having: list):
        self._having.append(having)
        return self

    def entityName(self, entityName: str):
        self._entityName = entityName
        return self


    """
  public function addPrefix($prefix){
    $this->addPrefixRecursive($this->condition, $prefix);
    
    foreach($this->order as $k=>$v){
      $this->order[$prefix.$k] = $v;
      unset($this->order[$k]);
    }
    return $this;
  }

  protected function removePrefixRecursive(array &$condition, $prefix){
    if(!key_exists(0, $condition)) return;
    if(is_array($condition[0])) {
      foreach($condition as &$value) $this->removePrefixRecursive($value,$prefix);  
    } else {
      $count = 1;
      $condition[0] = str_replace($prefix, '', $condition[0], $count);
    }
    return $this;
  }

  public function removePrefix($prefix){
    $this->removePrefixRecursive($this->condition, $prefix);
    
    foreach($this->order as $k=>$v){
      $count = 1;
      $newk = str_replace($prefix, '', $k, $count);
      $this->order[$newk] = $v;
      unset($this->order[$k]);
    }
    return $this;
  }

  public function unique(array $params){
    /**
     * definir condicion para campos unicos
     * $params:
     *   array("nombre_field" => "valor_field", ...)
     * los campos unicos simples se definen a traves del atributo Entity::$unique
     * los campos unicos multiples se definen a traves del atributo Entity::$uniqueMultiple
     */
    $uniqueFields = $this->container->entity($this->entityName)->unique;
    $uniqueFieldsMultiple = $this->container->entity($this->entityName)->uniqueMultiple;

    $condition = array();
    if(array_key_exists("id",$params) && !empty($params["id"])) array_push($condition, ["id", "=", $params["id"]]);

    foreach($uniqueFields as $field){
      foreach($params as $key => $value){
        if(($key == $field) && !empty($value)) {
          array_push($condition, [$key, "=", $value, "or"]);
        }
      }
    }

    if($uniqueFieldsMultiple) {
      $conditionMultiple = [];
      $first = true;
      $existsConditionMultiple = true; //si algun campo de la condicion multiple no se encuentra definido,  se carga en true.
      foreach($uniqueFieldsMultiple as $field){
        if(!$existsConditionMultiple) break;
        $existsConditionMultiple = false;
        
        foreach($params as $key => $value){
          if($key == $field) {
            $existsConditionMultiple = true;
            if($first) {
              $con = "or";
              $first = false;
            } else {
              $con = "and";
            }
            array_push($conditionMultiple, [$key, "=", $value, $con]);
          }
        }
      }

      if($existsConditionMultiple && !empty($conditionMultiple)) array_push($condition, $conditionMultiple);
    }

    if(empty($condition)) throw new Exception("Error al definir condicion unica");

    $this->cond($condition);
    return $this;
  }


  /**
     * Retorna la columna indicada en el parametro
     * @example $render->fields(["id","nombres"])->column();
     * @example $render->fields(["_count"])->column();
     */
  public function column($number = 0){
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

  /**
   * Definir SQL
   */
  public function sql() {
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


  protected function mapping($fieldName){
     /**
     * Interpretar prefijo y obtener mapping
     */
    $f = $this->container->explodeField($this->entityName, $fieldName);
    $m = $this->container->mapping($f["entity_name"], $f["field_id"]);
    return [$m, $f["field_name"]];
  }

  protected function fieldsQuery(){
    $fields = array_merge($this->group, $this->fields);

    $fieldsQuery_ = [];
    foreach($fields as $key => $fieldName){
      if(is_array($fieldName)){
        if(is_integer($key)) throw new Exception("Debe definirse un alias para la concatenacion (key must be string)");
        $map_ = [];
        foreach($fieldName as $fn){
          $f = $this->container->explodeField($this->entityName, $fn);
          $m = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
          array_push($map_, $m);
        } 
        $f = "CONCAT_WS(', ', " . implode(",",$map_) . ") AS " . $key;
      } else {
        $f = $this->container->explodeField($this->entityName, $fieldName);
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


  protected function groupBy(){
    $group_ = [];
    foreach($this->group as $key => $fieldName){
      if(is_array($fieldName)){
        if(is_integer($key)) throw new Exception("Debe definirse un alias para la concatenacion (key must be string)");
        $f = $key;
      } else {
        $f = $this->container->explodeField($this->entityName, $fieldName);
        $map = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
      }
      array_push($group_, $map);
    }

    return empty($group_) ? "" : "GROUP BY " . implode(", ", $group_) . "
";
  }

  protected function join(){
    $sql = "";
    $tree = $this->container->tree($this->entityName);
    $this->joinFk($tree, "", $sql);
    return $sql;
  }

  protected function joinFk(array $tree, $tablePrefix, &$sql){
    if (empty ($tablePrefix)) $tablePrefix = $this->container->entity($this->entityName)->getAlias();

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

" . $this->container->entity($this->entityName)->sn_() . "

 AS {$this->container->entity($this->entityName)->getAlias()}
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
      if(!$condition) throw new Exception("No pudo definirse el SQL de la condicion del campo: {$this->entityName}.{$field}");
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
    $f = $this->container->explodeField($this->entityName, $field);

    if(strpos($value, FF) === 0) { //definir condicion entre fields
      $v = $this->container->explodeField($this->entityName, substr($value, strlen(FF)));
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
     *    entityName = "persona"
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
    $entity = $this->container->entity($this->entityName);
    $orderDefault = (!empty($entity->getOrderDefault())) ? $entity->getOrderDefault() : array_fill_keys($entity->main, "asc"); //se retorna ordenamiento por defecto considerando campos principales nf de la entidad principal

    foreach($this->order as $key => $value) {
      if(array_key_exists($key, $orderDefault)) unset($orderDefault[$key]);
    }

    $order = array_merge($this->order, $orderDefault);
    
    $sql = '';
    foreach($order as $key => $value){
      $value = ((strtolower($value) == "asc") || ($value === true)) ? "asc" : "desc";
      $f = $this->container->explodeField($this->entityName, $key);
      $map_ = $this->container->mapping($f["entity_name"], $f["field_id"])->_($f["field_name"]);
      $sql_ = "{$map_} IS NULL, {$map_} {$value}";
      $sql .= concat($sql_, ', ', ' ORDER BY', $sql);
    }
    return $sql;
  }
}

"""