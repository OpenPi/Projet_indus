<?php

    require_once("../orm/Measure.php");

    //Retrieve the optionnal param to filter response
    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";

    //Retrive the ID of measures required
    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    $tableObject = new Measure();

    //If both of parameter are not given get all measures
    if($xlast == "undefined" and $time == "undefined"){
        //If id in url select device selected
        if($id != ""){
            $cond = array("hardwareConfigurationId" => array("=", $id));
            $res = $tableObject->getRows($cond);
        }
        else{
            $res = $tableObject->getAll();
        }
    }
    //If both parameter are given get data
    else if($xlast != "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=", $time));
        if($id != ""){
            $cond += array("hardwareConfigurationId" => array("=", $id));
        }
	   $res = $tableObject->getRowsLimited($cond, $xlast);
    }
    //If xlast alone
    else if($xlast != "undefined" and $time == "undefined"){
        if($id != ""){
            $cond = array("hardwareConfigurationId" => array("=", $id));
            $res = $tableObject->getRowsLimited($cond, $xlast);
        }else{
	       $res = $tableObject->getAllLimited($xlast);
        }
    }
    //If filter by timestamp
    else if($xlast == "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=",$time));
        //ID ressource in url
        if($id != ""){
            $cond += array("hardwareConfigurationId" => array("=", $id));
        }
	    $res = $tableObject->getRows($cond);
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