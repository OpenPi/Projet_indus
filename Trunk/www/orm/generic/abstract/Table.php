<?php

/**
    * @file Table.php
    * @author Cédric Delhaes
    * @version 1.0
    * @date 25/02/2015
    * @brief This class contains functions to read/write/delete from the database
**/

abstract class Table{

	protected $db; //!< Database
	protected $name; //!< table name
	protected $fields; //!< Field name in database and name userfrindly to respond
	protected $all; //!< Redifine all selection with user friendly name
	
	/**
            * @brief This function returns the entire table
            * @return $allRows Data list
        **/
	public function getAll(){
		$query = "SELECT ".$this->all." FROM ".$this->name;
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

		$query = "SELECT ".$this->all." FROM ".$this->name." LIMIT 0,".$limit;
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
            $where = substr_replace($where, "", -5, 5).";";
            $query = "SELECT ".$this->all." FROM ".$this->name." WHERE ".$where;
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
            $query = "SELECT ".$this->all." FROM ".$this->name." WHERE ".$where." LIMIT 0,".$limit;
            $rows = $this->db->getResponse($query);
            return $rows;
	}
	

	/**
            * Inserting rows into a table
            * @param $valeurs value list to insert
            * @return $idInsere id of the inserted row
        */
	public function insertRow($valeurs){
	
		$queryInsertRow = "INSERT INTO ".$this->name."(";
		
		$allField = array_keys($this->fields);
		
		// TODO regarder si il y a autant de valeur que de champs
		for($i = 0; $i < count($allField); $i++){
		
			$queryInsertRow .= $allField[$i].",";
		}
		
		$queryInsertRow = substr_replace($queryInsertRow, "", -1, 1);
		$queryInsertRow .= ") VALUES(".$valeurs.");";
		
		//echo $queryInsertRow;

		$this->db->executeQuery($queryInsertRow);
		
		// Retourne l'id de la ligne insere
		$resultQuery = $this->db->executeQuery("SELECT  LAST_INSERT_ID()");
		
		while( $row = mysqli_fetch_assoc($resultQuery) ){
			
				$idInsere = $row['LAST_INSERT_ID()'];
		}
		
		return $idInsere;
		
	}
	
	/**
            * Delete rows into a table according to conditions
            * @param $cond delete condition
            * @return 0
        */
	public function deleteRow($cond){
	
		$queryDeleteRow = "DELETE FROM ".$this->name." WHERE ";
		
		$where ="";
		
		reset($cond);
		while (list($key, $val) = each($cond)) {
		
			if( !array_key_exists($key, $this->fields) ){
			
				echo "<br><br> PROBLEME => Le champ ".$key." n'existe pas ! <br><br>";
				return -1;
			}
			
			$queryDeleteRow .= $key."=".$val." AND ";
		}
		
		$queryDeleteRow = substr_replace($queryDeleteRow, "", -5, 5).";";
		
		$this->db->executeQuery($queryDeleteRow);
		
		return 0;
		
	}
	
	/**
            * Update rows into a table according to conditions
            * @param $newValue update value
            * @param $cond update condition
            * @return -1 if problem
        */
	public function updateRow($newValue, $cond){
		$queryUpdateRow = "UPDATE ".$this->name." SET ";
		
		reset($newValue);
		while (list($key, $val) = each($newValue)) {
		
			if( !array_key_exists($key, $this->fields) ){
			
				echo "<br><br> PROBLEME => Le champ ".$key." n'existe pas ! <br><br>";
				return -1;
			}
			
			$queryUpdateRow .= $key."=".$val.", ";
		}
		
		$queryUpdateRow = substr_replace($queryUpdateRow, "", -2, 2)." WHERE ";
		
		reset($cond);
		while (list($key, $operator_value) = each($cond)) {
		
			if( !array_key_exists($key, $this->fields) ){
			
				echo "<br><br> PROBLEME => Le champ ".$key." n'existe pas ! <br><br>";
				return -1;
			}
			if( !in_array($operator_value[0], array("<",">","=","<=",">=")) ){
                    echo "<br><br> PROBLEME : Operator ".$operator_value[0]." doesn't exist ! <br><br>";
                    return $rows;
                }	
			
			$queryUpdateRow .= $key.$operator_value[0].$operator_value[1]." AND ";
		}
		
		$queryUpdateRow = substr_replace($queryUpdateRow, "", -5, 5).";";
		$this->db->executeQuery($queryUpdateRow);
	}

	
	/**
            * Database deconnect
        */
	public function deconnect(){

        $this->db->deconnect();
    }
	
}

?>
