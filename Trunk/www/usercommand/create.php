<?php

    require_once("../orm/UserCommand.php");

    $command = isset ($_POST["command"]) ? $_POST["command"] : "undefined";
    $targetName  = isset ($_POST["targetName"]) ? $_POST["targetName"] : "undefined";
    $value  = isset ($_POST["value"]) ? $_POST["value"] : "undefined";

    if($command == "undefined" or $targetName == "undefined" or $value == "undefined"){
        die("Wrong parameters");
    }
    else{
        $tableObject = new UserCommand();
        $date = date('Y-m-d h:m:s');
echo $date;

        $tableObject->insertRow('"NULL", "'.$command.'", "'.$targetName.'", "'.$value.'", "'.$date.'", 0');

    }

	header('Content-Type: application/json');
	echo '{"sucess":true}';
?>