tribehr-kudo-givers
===================

Get the number of kudos given by each user on TribeHR. This is useful for things like manual badges that are based on the number of kudos given.

Setup
-----
1. Install Python 2.x.
2. `git clone git@github.com:andrewsf/tribehr-kudo-givers.git`
3. `cd tribehr-kudo-givers`
4. Edit config.ini:
	- subdomain (e.g., `lithium`)
    - username (e.g., `bob.barker@lithium.com`)
    - API key (Go to http://SUBDOMAIN.lithium.com/users/me/ and click "Edit Profile")


Running
-------
Run in the project directory:

    python script.py


Options
-------
To get a list of every kudo and its date (User A --> User B, 4 months ago), add to `config.ini`:

    verbose = true

Improvements
------------
This thing is super slow. That's because of Python's built-in `urllib2` module, which has hilariously terrible HTTP support. Switching to an external library like [requests](https://github.com/kennethreitz/requests) or [urllib3](https://github.com/shazow/urllib3) would be a great idea if I wanted to take on a third-party dependency.