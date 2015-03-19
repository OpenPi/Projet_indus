<?php

    require_once("../orm/Alert.php");

    //Retrieve the optionnal param to filter response
    $xlast = isset ($_GET["xlast"]) ? $_GET["xlast"] : "undefined";
    $time  = isset ($_GET["time"]) ? $_GET["time"] : "undefined";
    $viewed  = isset ($_GET["viewed"]) ? $_GET["viewed"] : "undefined";

    if($viewed != "undefined" && $viewed != 0 && $viewed != 1){
        $output["code"] = 400;
        $output["message"] = "Bad parameters";

        header('HTTP/1.1 400 Bad Request');
    }
    else{
        //Retrive the ID of measures required
        $id  = explode('/', $_SERVER['PATH_INFO'])[1];

        $tableObject = new Alert();

        //If both of parameter are not given get all measures
        if($xlast == "undefined" and $time == "undefined"){
            //If id in url select device selected
            if($viewed != "undefined" || $id != ""){
                $cond = [];
                if($id != ""){
                    $cond += array("hardwareConfigurationId" => array("=", $id));
                }
                if($viewed != "undefined"){
                    $cond += array("shown" => array("=", $viewed));
                }
                $res = $tableObject->getRows($cond);
            }
            else{
                $res = $tableObject->getAll();
            }
        }
        //If both parameter are given get data
        else if($xlast != "undefined" and $time != "undefined"){
            $cond = array("timestamp" => array(">=", $time));
            if($viewed != "undefined" || $id != ""){
                if($id != ""){
                    $cond += array("hardwareConfigurationId" => array("=", $id));
                }
                if($viewed != "undefined"){
                    $cond += array("shown" => array("=", $viewed));
                }
                $res = $tableObject->getRows($cond);
            }
           $res = $tableObject->getRowsLimited($cond, $xlast);
        }
        //If xlast alone
        else if($xlast != "undefined" and $time == "undefined"){
            if($viewed != "undefined" || $id != ""){
                $cond = [];
                if($id != ""){
                    $cond += array("hardwareConfigurationId" => array("=", $id));
                }
                if($viewed != "undefined"){
                    $cond += array("shown" => array("=", $viewed));
                }
                $res = $tableObject->getRows($cond);
            }{
               $res = $tableObject->getAllLimited($xlast);
            }
        }
        //If filter by timestamp
        else if($xlast == "undefined" and $time != "undefined"){
            $cond = array("timestamp" => array(">=",$time));
            //ID ressource in url
            if($viewed != "undefined" || $id != ""){
                if($id != ""){
                    $cond += array("hardwareConfigurationId" => array("=", $id));
                }
                if($viewed != "undefined"){
                    $cond += array("shown" => array("=", $viewed));
                }
                $res = $tableObject->getRows($cond);
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
    }
?>