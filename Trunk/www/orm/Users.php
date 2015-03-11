<?php

require_once("generic/Db.php");
require_once("generic/abstract/Table.php");

final class Users extends Table{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "users";
        $this->fields = array(
                "id"                      => "id",
                "name"                    => "name",
                "password"                => "password"
        );

        //Change database label by userfrindly label for the respond
        $this->all = "";
        foreach ($this->fields as $key => $value) {
             $this->all = $this->all.$this->name.".".$key." AS ".$value.", ";
        }
        $this->all = substr_replace($this->all, '', '-2');
    }
}

?>
