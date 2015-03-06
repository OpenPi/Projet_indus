<?php

    require_once('../orm/HardwareConfiguration.php');

    //Retrieve ID
    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    $tableObject = new HardwareConfiguration();

    if($id != ""){
        $cond = array("id" => array("=", $id));
        $res = $tableObject->getRows($cond);
    }
    else{
        $res = $tableObject->getAll();
    }
    
    $i= 0;
    $output["hardwareConfigurations"] = "";
    foreach ($res as $value) {
    	$output["hardwareConfigurations"][$i] = $value;
    	$i++;
    }
    header('HTTP/1.1 200 OK');

    if(empty($output["hardwareConfigurations"])){
        $output="";
        $output["code"]=404;
        $output["message"]= "Not found";

        header('HTTP/1.1 404 Not Found');
    }
?>