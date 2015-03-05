<?php

    require_once("../orm/Users.php");

    if($_SERVER['REQUEST_METHOD'] == 'GET'){

        $user = isset($_GET['user']) ? $_GET['user'] : 'undefined';
        $password = isset($_GET['password']) ? $_GET['password'] : 'undefined';

        if($user == 'undefined' OR $password == 'undefined'){
            $o["code"] = 400;
            $o["message"] = "Bad parameters";

            header('HTTP/1.1 400 Bad Request');
            header('Content-Type: application/json');

            echo json_encode($o);
            die();
        }

        $tableObject = new Users();
        
        $cond = array("name" => array("=", '"'.$user.'"'));
        $res = $tableObject->getRows($cond);
        

        if(sizeof($res) > 1){
            $o["code"] = 500;
            $o["message"] = "Something went wrong with the server";

            header('HTTP/1.1 500  Internal Server Error');
            header('Content-Type: application/json');
            echo json_encode($o);
            die();
        }
        else if(sizeof($res) == 0){
            $o["code"] = 401;
            $o["message"] = "Username and password invalid";

            header('HTTP/1.1 401  Internal Server Error');
            header('Content-Type: application/json');
            echo json_encode($o);
            die();
        }

        if($res[0]["password"] == $password){
            header('HTTP/1.1 200  OK');
            header('Content-Type: application/json');
            
            $o["token"] = sha1(date("Y-m-d H:i:s"));

            session_start();
            $_SESSION["user"] += $user;
            $_SESSION["token"] += $o["token"];

        }
        else{
            $o["code"] = 401;
            $o["message"] = "Username and password invalid";

            header('HTTP/1.1 401  Internal Server Error');
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