<?php
//Author:  Carlo Satta
//Description: Print all writable directories.
c('.');
function c($d){
	echo "Entro in ".$d."<br>";
	$h = opendir($d);
	while ($f = readdir($h)) {
		$df=$d.'/'.$f; 
		if((is_dir($df))&&($f!='.')&&($f!='..')){
			if(is_writable($df)) echo "Writable: ".$f."<br>";
			c($df);
			echo "Esco da ".$df."<br>";
		}
	}
	$h = closedir($h);
}
?>
