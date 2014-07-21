import ConfigParser
import sys
import urllib2
from xml.etree import ElementTree


# Read config
try:
	parser = ConfigParser.SafeConfigParser()
	parser.read('config.ini')
	subdomain = parser.get('Config', 'subdomain').strip()
	username = parser.get('Config', 'username').strip()
	apikey = parser.get('Config', 'apikey').strip()
except ConfigParser.Error as e:
	print 'Failed to read config:', e
except ConfigParser.NoOptionError as e:
	print 'Option missing:', e
	sys.exit(1)

if not subdomain:
	print 'Config file is missing subdomain.'
	sys.exit(1)
if not username:
	print 'Config file is missing username.'
	sys.exit(1)
if not apikey:
	print 'Config file is missing apikey.'
	sys.exit(1)

print 'Accessing %s.mytribehr.com on behalf of user %s...' % (subdomain, username)
domain = '%s.mytribehr.com' % subdomain
uriPrefix = 'http://%s/' % domain

# Set up authentication
auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(realm=domain, uri=uriPrefix, user=username, passwd=apikey)
opener = urllib2.build_opener(auth_handler)

#debug_handler=urllib2.HTTPSHandler(debuglevel=1)
#opener = urllib2.build_opener(debug_handler, auth_handler)

urllib2.install_opener(opener)

response = urllib2.urlopen(uriPrefix + 'users.xml')
rootElem = ElementTree.parse(response).getroot()
response.close()

userElems = rootElem.findall('user')
print 'Found', len(userElems), 'users'
for userElem in userElems:
	print userElem.get('id'), ':', userElem.get('full_name')
