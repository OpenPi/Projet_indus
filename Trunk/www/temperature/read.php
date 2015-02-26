<?php

    require_once("../orm/Temperature.php");

    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";

    $tableObject = new Temperature();

    //If both of parameter are not given stop process
    if($xlast == "undefined" and $time == "undefined"){
	$res = $tableObject->getAll();
    }
    //If both parameter are given get data
    else if($xlast != "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=",$time));
	$res = $tableObject->getRowsLimited($cond, $xlast);
    }
    //If xlast alone
    else if($xlast != "undefined" and $time == "undefined"){
	$res = $tableObject->getAllLimited($xlast);
    }
    //If time alone
    else if($xlast == "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=",$time));
	$res = $tableObject->getRows($cond);
    }
    
    $i= 0;
    $o["measures"] = "";

	foreach ($res as $value) {
		$o["measures"][$i] = $value;
		$i++;
	}

	header('Content-Type: application/json');
	echo json_encode($o);
?>