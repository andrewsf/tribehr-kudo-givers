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

	try:
		verbose = parser.get('Config', 'verbose').strip().lower() == 'true'
	except ConfigParser.Error as e:
		verbose = False

except ConfigParser.NoOptionError as e:
	print 'Option missing:', e
except ConfigParser.Error as e:
	print 'Failed to read config:', e
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
usersRootElem = ElementTree.parse(response).getroot()
response.close()

totalKudos = 0
userKudosGiven = {}
userKudosReceived = {}
userUniqueKudosGiven = {}

# Process users
userElems = usersRootElem.findall('user')
userCount = len(userElems)
print 'Found', userCount, 'users. Getting kudos (this will take a while)...'

progress = 0
lastShownMilestone = 0
for userElem in userElems:
	userId = userElem.get('id')
	response = urllib2.urlopen(uriPrefix + 'users/' + userId + '/kudos.xml')
	notesRootElem = ElementTree.parse(response).getroot()
	response.close()

	# Process kudos
	noteElems = notesRootElem.findall('note')

	# Users with no kudos have one empty <note> element
	if len(noteElems) <= 0 or noteElems[0].get('is_kudo') != '1':
		if verbose:
			print '%s has no kudos. :(' % userElem.get('full_name')
		continue

	userKudosReceived[userId] = len(noteElems)

	for noteElem in noteElems:
		posterElem = noteElem.find('poster')
		if verbose:
			print '%s --> %s, %s' % (posterElem.get('full_name'), userElem.get('full_name'), noteElem.get('created'))

		giver = noteElem.get('poster_id')
		userKudosGiven[giver] = userKudosGiven.get(giver, 0) + 1
		totalKudos += 1

	progress += 1

	# Get progress percentage, output if crossing a 5% milestone. Don't show 100%.
	percentMilestone = int(progress * 20 / userCount) * 5
	if percentMilestone > lastShownMilestone and percentMilestone < 100:
		print '%s%% complete -- %s kudos tracked' % (percentMilestone, totalKudos)
		lastShownMilestone = percentMilestone

print 'Done! %s kudos tracked in total.' % totalKudos
print '%s users have no kudos! :(' % (len(userElems) - len(userKudosReceived))




print ''


