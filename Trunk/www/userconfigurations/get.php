<?php

    require_once('../orm/UserConfiguration.php');

    //Retrieve ID (RESTFUl)
    $id  = explode('/', $_SERVER['PATH_INFO'])[1];

    $tableObject = new UserConfiguration();

    //If ID exist get information from database about configuration
    if($id != ""){
        $cond = array("id" => array("=", $id));
        $res = $tableObject->getRows($cond);
    }
    //Else get all configuration
    else{
        $res = $tableObject->getAll();
    }
    
    //Create JSON with information
    $i= 0;
    $output["userconfigurations"] = "";
    foreach ($res as $value) {
        $output["userconfigurations"][$i] = $value;
        $i++;
    }
    header('HTTP/1.1 200 OK');

    //In case JSON is empty change output
    if(empty($output["userconfigurations"])){
        $output="";
        $output["code"]=404;
        $output["message"]= "Not found";

        header('HTTP/1.1 404 Not Found');
    }
?>