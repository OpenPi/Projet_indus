<?php

require_once("Db.php");
require_once("Table.php");

final class Users extends Table{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "users";
        $this->fields = array(
                "id"                      => "id",
                "name"                    => "name",
                "password"                => "password"
        );
    }
}

?>
