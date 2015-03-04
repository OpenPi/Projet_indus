<?php

    require_once("../orm/UserCommand.php");

    $tableObject = new UserCommand();

    if($_SERVER['REQUEST_METHOD'] == 'POST'){
        $command = isset ($_POST["command"]) ? $_POST["command"] : "undefined";
        $targetName  = isset ($_POST["targetName"]) ? $_POST["targetName"] : "undefined";
        $value  = isset ($_POST["value"]) ? $_POST["value"] : "undefined";

        if( $command == "undefined" OR $targetName == "undefined" OR $value == "undefined"){
            $o["code"] = 400;
            $o["message"] = "Bad parameters";

            header('HTTP/1.1 400 Bad Request');
            header('Content-Type: application/json');
            echo json_encode($o);

            die();
        }

        $date = date("Y-m-d H:i:s");
        $tableObject->insertRow("'NULL', '".$command."', '".$targetName."', '".$value."', '".$date."', 0");

        $o["code"] = 201;
        $o["message"] = "Data created";

        header('HTTP/1.1 201 Created');
        header('Content-Type: application/json');
    }
    else if($_SERVER['REQUEST_METHOD'] == 'GET'){

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
    $o["commandes"] = "";

	foreach ($res as $value) {
		$o["commandes"][$i] = $value;
		$i++;
	}

    header('HTTP/1.1 200 OK');
    header('Content-Type: application/json');

    if(empty($o["commandes"])){
        $o = "";
        $o["code"] = 404;
        $o["message"] = "Not found";

        header('HTTP/1.1 404 Not Found');
        header('Content-Type: application/json');
    }
}
else{
    $o["code"] = 405;
    $o["message"] = "Methode ".$_SERVER['REQUEST_METHOD']." not allowed";

    header('HTTP/1.1 405 Method Not Allowed');
    header('Content-Type: application/json');
}

	echo json_encode($o);
?>