<?php

    require_once("../orm/Measure.php");

    //Retrieve the optionnal param to filter response
    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";
    $hardware_id  = isset ($_GET["hardware"]) ? $_GET["hardware"] : "undefined";

    //Retrive the ID of measures required
    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    $tableObject = new Measure();

    $cond = [];

    if($id != ""){
            $cond = array("id" => array("=", $id));
    }
    if($time != "undefined"){
            $cond += array("timestamp" => array(">=", $time));
    }
    if($hardware_id != "undefined"){
            $cond += array("hardwareConfigurationId" => array("=", $hardware_id));
    }

    if($xlast != "undefined"){
        //If filtring on date and condition
        if(count($cond) != 0){
            $res = $tableObject->getRowsLimited($cond, $xlast);
        } else {
            $res = $tableObject->getAllLimited($xlast);
        }
    } else {
        if(count($cond) != 0){
            $res = $tableObject->getRows($cond);
        } else {
            $res = $tableObject->getAll();
        }
    }
  
    //Insert database result in the output
    $i= 0;
    $output["measures"] = "";
	foreach ($res as $value) {
		$output["measures"][$i] = $value;
		$i++;
	}
    header('HTTP/1.1 200 OK');

    //If output is empty respond ressource not found
    if(empty($output["measures"])){
        //Clean the output
        $output="";
        $output["code"]=404;
        $output["message"]= "The ressource you search was not found";

        header('HTTP/1.1 404 Not Found');
    }
?>