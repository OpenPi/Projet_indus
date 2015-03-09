<?php
//Check the user authorization
if(isset($_SESSION['user']))
{
    //Check the HTTP Verb and select the right header
    switch($_SERVER['REQUEST_METHOD']){
        case 'GET':
            require_once('get.php');
            break;
        case 'PUT':
            header('HTTP/1.1 405 Method Not Allowed');

            $output['code'] = 405.1;
            $output['message'] = 'Methode '.$_SERVER['REQUEST_METHOD'].' not allowed';
            break;
        case 'POST':
            include_once('post.php');
            break;
        case 'DELETE':
            header('HTTP/1.1 405 Method Not Allowed');

            $output['code'] = 405.1;
            $output['message'] = 'Methode '.$_SERVER['REQUEST_METHOD'].' not allowed';
            break;
        default:
            header('HTTP/1.1 405 Method Not Allowed');

            $output['code'] = 405.1;
            $output['message'] = 'Methode '.$_SERVER['REQUEST_METHOD'].' not allowed';
            break;
    }
//User are not authorized
}else{
    header('HTTP/1.1 401 Unauthorized');

    $output['code'] = 401;
    $output['message'] = 'You need to be identificated to have access to this data';
}
header('Content-Type: application/json');
echo json_encode($output);
?>