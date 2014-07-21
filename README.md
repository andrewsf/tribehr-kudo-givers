tribehr-kudo-givers
===================

Get the number of kudos given by each user on TribeHR. This is useful for things like manual badges that are based on the number of kudos given.

Setup
-----
1. Install Python 2.x.
2. `git clone git@github.com:andrewsf/tribehr-kudo-givers.git`
3. `cd tribehr-kudo-givers`
4. `chmod +x script.py`
5. Edit config.ini:
	- subdomain (e.g., `lithium`)
    - username (e.g., `bob.barker`)
    - API key (Go to http://SUBDOMAIN.lithium.com/users/me/ and click "Edit Profile")


Running
-------
`./script.py`