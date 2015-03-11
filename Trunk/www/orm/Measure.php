<?php

require_once("generic/Db.php");
require_once("generic/abstract/TableJoinedTimestamped.php");

final class Measure extends TableJoinedTimestamped{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "measure";
        $this->field = "hardwareConfigurationId";
        $this->name_joined = "hardwareconfiguration";
        $this->field_joined = "id";
        $this->fields = array(
                "id"                           => "measure_id",
                "hardwareConfigurationId"      => "hardware_id",
                "value"                        => "value",
                "timestamp"                    => "timestamp",
        );

        //Change database label by userfrindly label for the respond
        $this->all = "";
        foreach ($this->fields as $key => $value) {
             $this->all = $this->all.$this->name.".".$key." AS ".$value.", ";
        }
        $this->all = $this->all.$this->name_joined.".name AS hardware_name";
        //$this->all = substr_replace($this->all, '', '-2');
    }
}

?>
