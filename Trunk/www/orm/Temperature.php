<?php

require_once("Db.php");
require_once("MeasureSensor.php");

final class Temperature extends MeasureSensor{
	
    public function __construct(){
        $this->db = new Db();
        $this->name = "measure";
        $this->fields = array(
                "id"                           => "id",
                "hardwareConfigurationId"      => "hardwareConfigurationId",
                "value"                        => "value",
                "timestamp"                    => "timestamp",
        );
        $this->sensor_name = "capteur temperature";
        $this->hardwareTable = "hardwareConfiguration";
    }
	
}

?>
