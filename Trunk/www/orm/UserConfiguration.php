<?php

require_once("Db.php");
require_once("Table.php");

final class Measure extends Table{
	
    public function __construct(){

        $this->db = new Db();
        $this->name = "userConfiguration";
        $this->fields = array(
                "id"                       => "id",
                "name"                     => "name",
                "unit"                     => "unit",
                "value"                    => "value",
        );
    }
	
}

?>
