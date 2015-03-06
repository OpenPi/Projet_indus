<?php
    session_start();
    //Check if session started and destroy it
    if(isset($_SESSION['user'])){
        session_destroy();
        header('HTTP/1.1 200 OK');

        $output['code'] = 200;
        $output['message'] = 'You are disconnected';
    //Or inform that no session available to destroy
    }else{
        header('HTTP/1.1 400 Bad Request');

        $output['code'] = 400;
        $output['message'] = 'You are already disconnected';
    }
?>