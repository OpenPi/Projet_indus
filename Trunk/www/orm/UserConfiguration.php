<?php

require_once("generic/Db.php");
require_once("generic/abstract/TableJoined.php");

final class UserConfiguration extends TableJoined{

    public function __construct(){
        $this->db = new Db();
        $this->name = "userconfiguration";
        $this->field = "hardwareConfigurationId";
        $this->name_joined = "hardwareconfiguration";
        $this->field_joined = "id";
        $this->fields = array(
                "id"                          => "id",
                "name"                        => "name",
                "hardwareConfigurationId"     => "hardware_id",
                "unit"                        => "unit",
                "value"                       => "value"
        );

        $this->hardwareTable = "hardwareconfiguration";

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
