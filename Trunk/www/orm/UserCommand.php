<?php

require_once("generic/Db.php");
require_once("generic/abstract/TableTimestamped.php");

final class UserCommand extends TableTimestamped{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "usercommand";
        $this->fields = array(
                "id"             => "id",
                "type"           => "type",
                "command"        => "command",
                "targetName"     => "name",
                "value"          => "value",
                "timestamp"      => "timestamp",
                "done"           => "done",
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
