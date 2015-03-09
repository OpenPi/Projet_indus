<?php

require_once("Db.php");
require_once("Table.php");

final class HardwareConfiguration extends Table{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "hardwareconfiguration";
        $this->fields = array(
                "id"                      => "id",
                "name"                    => "name",
                "pin"                     => "pin",
                "IO"                      => "IO",
                "PullUpDownResistor"      => "PullUpDownResistor",
                "unit"                    => "unit",
                "tension"                 => "tension"
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
