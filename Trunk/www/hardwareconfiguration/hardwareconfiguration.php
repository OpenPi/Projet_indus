<?php

    require_once("../orm/HardwareConfiguration.php");

    if($_SERVER['REQUEST_METHOD'] == 'GET'){
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
        $o["hardwareConfigurations"] = "";

    	foreach ($res as $value) {
    		$o["hardwareConfigurations"][$i] = $value;
    		$i++;
    	}

        header('HTTP/1.1 200 OK');
        header('Content-Type: application/json');

        if(empty($o["hardwareConfigurations"])){
            $o="";
            $o["code"]=404;
            $o["message"]= "Not found";

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