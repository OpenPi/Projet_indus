<?php

    require_once("../orm/Alert.php");

    //Retrieve data parameters
    $_PUT  = array();    
    parse_str(file_get_contents('php://input'), $_PUT);  

    $id  = explode('/', $_SERVER['PATH_INFO'])[1];
    $show = isset($_PUT["show"]) ? $_PUT["show"] : "undefined";

    //Check if data was given
    if($id == "" || $show == "undefined"){
        $output["code"] = 400;
        $output["message"] = "Bad parameters";

        header('HTTP/1.1 400 Bad Request');      
    }
    else{
        //Check validity of show
        if($show == "0" || $show == "1"){
            $tableObject = new Alert();
            //Create condition to find row to update
            $cond = [];
            $cond += array("id" => array("=", $id));

            $date = date("Y-m-d H:i:s");

            $newValue = [];
            $newValue += array("timestamp" => "'".$date."'");

            //Send request to database
            if($show == "0"){
                $newValue += array("shown" => 0);
                echo $tableObject->updateRow($newValue, $cond);
            }else{
                $newValue += array("shown" => 1);
                echo $tableObject->updateRow($newValue, $cond);
            }
            $output["code"] = 200;
            $output["message"] = "OK update done";

            header('HTTP/1.1 200 OK');
        }
        else{
            $output["code"] = 400;
            $output["message"] = "Bad parameters";

            header('HTTP/1.1 400 Bad Request');            
        }
    }   
?>