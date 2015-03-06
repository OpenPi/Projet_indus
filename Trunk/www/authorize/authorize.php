<?php
//Check the HTTP Verb and select the right header
switch($_SERVER['REQUEST_METHOD']){
    case 'GET':
        header('HTTP/1.1 405 Method Not Allowed');

        $output['code'] = 405.1;
        $output['message'] = 'Methode '.$_SERVER['REQUEST_METHOD'].' not allowed';
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
        include_once('delete.php');
        break;
    default:
        header('HTTP/1.1 405 Method Not Allowed');

        $output['code'] = 405.1;
        $output['message'] = 'Methode '.$_SERVER['REQUEST_METHOD'].' not allowed';
        break;
}
header('Content-Type: application/json');
echo json_encode($output);
?>