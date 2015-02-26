<?php

require_once("Db.php");
require_once("Table.php");

final class UserCommand extends Table{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "userCommand";
        $this->fields = array(
                "id"             => "id",
                "command"        => "command",
                "targetName"     => "targetName",
                "value"          => "value",
                "timestamp"      => "timestamp",
                "done"           => "done",
        );
    }

    /**
        * @brief This function returns the entire table
        * @return $allRows Data list
    **/
    public function getAll(){
       $query = "SELECT *
                 FROM ".$this->name."
                 ORDER BY timestamp DESC";
        $allRows = $this->db->getResponse($query);	
        return $allRows;
    }

    /**
        * @brief This function returns the entire table limited in element
        * @param $limit select number max of element
        * @return $allRows Data list
    **/
    public function getAllLimited($limit){

	$query = "SELECT *
                 FROM ".$this->name."
                 ORDER BY timestamp DESC
                 LIMIT 0,".$limit;
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
            $query = "SELECT *
                 FROM ".$this->name."
                 WHERE ".$where."
                 ORDER BY timestamp DESC";
            $rows = $this->db->getResponse($query);
            return $rows;
	}

     /**
            * @brief Collect some tuples of a table after some content provided $cond table and limit.
            * @param $cond select conditions
            * @param $limit select number max of element
            * @return $rows Data list
     */
     public function getRowsLimited($cond, $limit){
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
            $query = "SELECT *
                 FROM ".$this->name."
                 WHERE ".$where."
                 ORDER BY timestamp DESC
                 LIMIT 0,".$limit;
            $rows = $this->db->getResponse($query);
            return $rows;
	}
	
}

?>
