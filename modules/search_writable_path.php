//Author:  Carlo Satta
//Description: Print all writable directories.
c($_SERVER['DOCUMENT_ROOT']);
function c($d){
	$h = opendir($d);
	while ($f = readdir($h)) {
		$df=$d.'/'.$f; 
		if((is_dir($df))&&($f!='.')&&($f!='..')){
			if(is_writable($df)) echo "Writable: ".str_replace($_SERVER['DOCUMENT_ROOT'],'',$df)."\n";
			c($df);
		}
	}
	closedir($h);
}
