<?php
    session_start();

    if(isset($_SESSION['user'])){
        session_destroy();
        header('HTTP/1.1 200 OK');

        $output['code'] = 200;
        $output['message'] = 'You are disconnected';
    }else{
        header('HTTP/1.1 400 Bad Request');

        $output['code'] = 400;
        $output['message'] = 'You are already disconnected';
    }
?>