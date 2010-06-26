//Description: Check and try to disable PHP safe_mode.
$s='safe_mode'; $o='open_basedir'; $d='disable_functions';
@ini_restore($s); @ini_set($s,0);
@ini_restore($o); @ini_set($o,'');
@ini_restore($d); @ini_set($d,'');
print($s . " = " . @ini_get('safe_mode') . "\n");
print($d . " = " . @ini_get('disable_functions') . "\n");
print($o . " = " . @ini_get('open_basedir') . "\n");