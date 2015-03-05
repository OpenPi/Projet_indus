<?php

require_once("Db.php");
require_once("Table.php");

final class HardwareConfiguration extends Table{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "hardwareConfiguration";
        $this->fields = array(
                "id"                      => "id",
                "name"                    => "name",
                "pin"                     => "pin",
                "IO"                      => "IO",
                "PullUpDownResistor"      => "PullUpDownResistor",
                "unit"                    => "unit",
                "tension"                 => "tension"
        );
    }
}

?>
