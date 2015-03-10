<?php

require_once("Db.php");
require_once("Table.php");

final class UserConfiguration extends Table{
	
    protected $hardwareTable;

    public function __construct(){
        $this->db = new Db();
        $this->name = "userconfiguration";
        $this->fields = array(
                "id"                          => "id",
                "name"                        => "name",
                "hardwareConfigurationId"     => "hardware_id",
                "unit"                        => "unit",
                "value"                       => "value"
        );

        $this->hardwareTable = "hardwareconfiguration";

        //Change database label by userfrindly label for the respond
        $this->all = "";
        foreach ($this->fields as $key => $value) {
             $this->all = $this->all.$this->name.".".$key." AS ".$value.", ";
        }
        $this->all = $this->all.$this->hardwareTable.".name AS hardware_name";
        //$this->all = substr_replace($this->all, '', '-2');
    }    

/**
        * @brief This function returns the entire table for the sensor
        * @return $allRows Data list
    **/
    public function getAll(){
       $query = "SELECT ".$this->all."
                 FROM ".$this->name."
                 INNER JOIN ".$this->hardwareTable."
                 WHERE ".$this->hardwareTable.".id=".$this->name.".hardwareConfigurationId";
        $allRows = $this->db->getResponse($query);  
        return $allRows;
    }

     /**
            * @brief Collect some tuples of a table after some content provided $cond table.
            * @param $cond select conditions
            * @return $rows Data list
     */
    public function getRows($cond){
            $where = "";
            $rows = array();
        
            reset($cond);

            while (list($key, $operator_value) = each($cond)) {
                if( !array_key_exists($key, $this->fields) ){
                    echo "<br><br> PROBLEME => Le champ ".$key." n'existe pas ! <br><br>";
                    return $rows;
                }
                if( !in_array($operator_value[0], array("<",">","=","<=",">=")) ){
                    echo "<br><br> PROBLEME : Operator ".$operator_value[0]." doesn't exist ! <br><br>";
                    return $rows;
                }
                $where .= $key."".$operator_value[0]."".$operator_value[1]." AND ";
            }
            $where = substr_replace($where, "", -5, 5)."";
            $query = "SELECT ".$this->all."
                 FROM ".$this->name."
                 INNER JOIN ".$this->hardwareTable."
                 WHERE ".$this->hardwareTable.".id=".$this->name.".hardwareConfigurationId AND ".$this->name.".".$where;
            $rows = $this->db->getResponse($query);
            return $rows;
    }
    
}

?>
