<?
    require_once("../orm/UserCommand.php");

    //Retrieve POST information
    $command     = isset ($_POST["command"]) ? $_POST["command"] : "undefined";
    $targetName  = isset ($_POST["targetName"]) ? $_POST["targetName"] : "undefined";
    $value       = isset ($_POST["value"]) ? $_POST["value"] : "undefined";

    //Check validity
    if( $command == "undefined" OR $targetName == "undefined" OR $value == "undefined"){
        $output["code"] = 400;
        $output["message"] = "Bad parameters";

        header('HTTP/1.1 400 Bad Request');
    }
    //Insert data in database
    else{
        $tableObject = new UserCommand();
    
        $date = date("Y-m-d H:i:s");
        $tableObject->insertRow("'NULL', '".$command."', '".$targetName."', '".$value."', '".$date."', 0");

        $output["code"] = 201;
        $output["message"] = "Data created";

        header('HTTP/1.1 201 Created');
    }
?>