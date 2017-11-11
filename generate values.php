<?php
/*
 * Genereert wat willekeurige waardes en gooit ze in een database
 * Houdt vaag rekening met een dag en nacht ritme, maar geeft wel erg spikey waardes
 */
    $startTime  = new \DateTime('2017-11-01 00:00');
    $endTime    = new \DateTime('2017-11-11 23:55');
    $timeStep   = 1;
    $timeArray  = array();
    $servername = "localhost";
    $username = "root";
    $database = "project21";

    while($startTime <= $endTime)
    {
    #$timeArray[] = $startTime->format('H:i');
        $h = $startTime->format('H');
        if($h < 5 || $h > 22){
            $m = rand(0, 20);
        } elseif ($h >= 5 && $h <= 8){
            $m = rand(20, 50);
        } elseif ($h >= 9 && $h <= 10){
            $m = rand(50, 80);
        } elseif ($h >= 11 && $h <= 15){
            $m = rand(80, 120);
        } elseif ($h >= 16 && $h <= 20){
            $m = rand(50, 80);
        } elseif ($h >= 21 && $h <= 22){
            $m = rand(20, 50);
        }

        $temp = 16;
        $licht = 90;
        echo $startTime->format('H:i'),' ', ($licht*$m/100),' ', ($temp*$m/100), ' ', $m, "\r\n";

        $conn = new mysqli($servername, $username, db_name=$database);



        $conn->close();
    $startTime->add(new \DateInterval('PT'.$timeStep.'M'));
    }

    echo json_encode($timeArray);
?>