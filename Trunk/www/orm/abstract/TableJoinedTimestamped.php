<?php

require_once("Table.php");

/**
    * @file TableTimestamped.php
    * @author Cédric Delhaes
    * @version 1.0
    * @date 25/02/2015
    * @brief This class contains functions to read/write/delete from the database with a table and a inner join
**/

abstract class TableJoinedTimestamped extends Table{

	protected $db; //!< Database
	protected $name; //!< table name
    protected $field; //!< field to join table 1
    protected $name_joined; //!< table name of second table
    protected $field_joined; //!< field to join table 2
	protected $fields; //!< Field name in database and name userfrindly to respond
	protected $all; //!< Redifine all selection with user friendly name
	
    /**
        * @brief This function returns the entire table for the sensor
        * @return $allRows Data list
    **/
    public function getAll(){
       $query = "SELECT ".$this->all."
                 FROM ".$this->name."
                 INNER JOIN ".$this->name_joined."
                 WHERE ".$this->name_joined.".".$this->field_joined."=".$this->name.".".$this->field."
                 ORDER BY timestamp DESC";
        //echo $query;
        $allRows = $this->db->getResponse($query);  
        return $allRows;
    }

    /**
        * @brief This function returns the entire table limited in element
        * @param $limit select number max of element
        * @return $allRows Data list
    **/
    public function getAllLimited($limit){
    	$query = "SELECT ".$this->all."
                     FROM ".$this->name."
                     INNER JOIN ".$this->name_joined."
                     WHERE ".$this->name_joined.".".$this->field_joined."=".$this->name.".".$this->field."
                     ORDER BY timestamp DESC
                     LIMIT 0,".$limit;
        //echo $query;
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
                 INNER JOIN ".$this->name_joined."
                 WHERE ".$this->name_joined.".".$this->field_joined."=".$this->name.".".$this->field." AND ".$this->name.".".$where."
                 ORDER BY timestamp DESC";
            //echo $query;
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
            $query = "SELECT ".$this->all."
                 FROM ".$this->name."
                 INNER JOIN ".$this->name_joined."
                 WHERE ".$this->name_joined.".".$this->field_joined."=".$this->name.".".$this->field." AND ".$this->name.".".$where."
                 ORDER BY timestamp DESC
                 LIMIT 0,".$limit;
            //echo $query;
            $rows = $this->db->getResponse($query);
            return $rows;
	}
	
}

?>
