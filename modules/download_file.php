print_r($ar);
echo file_put_contents($ar[1], file_get_contents($ar[0]))."\n";
