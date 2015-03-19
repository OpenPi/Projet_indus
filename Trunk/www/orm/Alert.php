<?php

require_once("generic/Db.php");
require_once("generic/abstract/TableJoinedTimestamped.php");

final class Alert extends TableJoinedTimestamped{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "alerts";
        $this->field = "hardwareConfigurationId";
        $this->name_joined = "hardwareconfiguration";
        $this->field_joined = "id";
        $this->fields = array(
                "id"                           => "alert_id",
                "hardwareConfigurationId"      => "hardware_id",
                "name"                         => "alert_name",
                "description"                  => "alert_description",
                "timestamp"                    => "timestamp",
                "shown"                        => "is_viewed"
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
