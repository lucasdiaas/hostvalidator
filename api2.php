<?php

function searchHost($hostname){

    $data = [
        'jsonrpc' => '2.0',
        'method' => 'getAccountSearch',
        'params' => [
            'authToken' => '2f8fac337afbc35bbb628dea68f43ba29db3a447b0371ad31569675a774edb3c',
    //        'id' => '11',
            'userPass' => 'UnIx2018',
            'text' => $hostname,
    //        'categoryId' => '5',
    //        'customerId' => '1',
    //        'pass' => '1234',
    //        'login' => 'root',
    //        'url' => 'http://syspass.org',
    //        'notes' => 'pruebaaaaaaa'
        ],
        'id' => 1
    ];
    $url = 'http://172.18.30.162/syspass/api.php';
    $content = json_encode($data);
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $content);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen($content),
            'Accept-Language: de_DE,en-US;q=0.7,en;q=0.3'
        )
    );
    $result = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($status != 200) {
        die("Error: call to URL $url failed with status $status, response $result, curl_error " . curl_error($ch) . ", curl_errno " . curl_errno($ch));
    }
    curl_close($ch);
    //var_dump(json_decode($result));
    echo $result;
}

//$server = readline();

$server = getopt("p:");

//if ($server !== false){
//    echo var_export($server, true);
//}

$host =  $server['p'];
