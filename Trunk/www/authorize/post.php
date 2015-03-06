<?php

    require_once('../orm/Users.php');

    //Retrieve user and password information 
    $user = isset($_POST['user']) ? $_POST['user'] : 'undefined';
    $password = isset($_POST['password']) ? $_POST['password'] : 'undefined';

    if($user != 'undefined' AND $password != 'undefined'){
        //Retrieve user and password from database
        $tableObject = new Users();
    
        $cond = array('name' => array('=', '"'.$user.'"'));
        $res = $tableObject->getRows($cond);

        //If database response more than one user
        if(sizeof($res) > 1){
            $output['code'] = 500;
            $output['message'] = 'Something went wrong with the server';
            header('HTTP/1.1 500  Internal Server Error');
        }
        //If user name not found
        else if(sizeof($res) == 0){
            $output['code'] = 401;
            $output['message'] = 'Username and password invalid';
            header('HTTP/1.1 401  Internal Server Error');
        }else{
            if($res[0]['password'] == $password){
                session_start();
                $_SESSION['user'] = $user;

                $output['code'] = 200;
                $output['message'] = 'You are now logged';
                header('HTTP/1.1 200  OK');
            }
            else{
                $output['code'] = 401;
                $output['message'] = 'Username and password invalid';
                header('HTTP/1.1 401  Internal Server Error');
            }
        }
    //If user name or password not given error
    }else{
        $output['code'] = 400;
        $output['message'] = 'Bad parameters';
        header('HTTP/1.1 400 Bad Request');
    }
?>