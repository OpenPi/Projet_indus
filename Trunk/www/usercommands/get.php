<?php

    require_once("../orm/UserCommand.php");

    $tableObject = new UserCommand();

    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";

    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    //If both of parameter are not given get all measures
    if($xlast == "undefined" and $time == "undefined"){
        //If id in url select device selected
        if($id != ""){
            $cond = array("id" => array("=", $id));
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
            $cond += array("id" => array("=", $id));
        }
	   $res = $tableObject->getRowsLimited($cond, $xlast);
    }
    //If xlast alone
    else if($xlast != "undefined" and $time == "undefined"){
        if($id != ""){
            $cond = array("id" => array("=", $id));
            $res = $tableObject->getRowsLimited($cond, $xlast);
        }
	   $res = $tableObject->getAllLimited($xlast);
    }
    //If time alone
    else if($xlast == "undefined" and $time != "undefined"){
        $cond = array("timestamp" => array(">=",$time));
        if($id != ""){
            $cond += array("id" => array("=", $id));
        }
	$res = $tableObject->getRows($cond);
    }
    
    $i= 0;
    $output["commandes"] = "";

	foreach ($res as $value) {
		$output["commandes"][$i] = $value;
		$i++;
	}

    header('HTTP/1.1 200 OK');

    if(empty($output["commandes"])){
        $output = "";
        $output["code"] = 404;
        $output["message"] = "Not found";

        header('HTTP/1.1 404 Not Found');
    }

?>