from django.db import connection
from django.conf import settings

from Crypto.Hash import SHA256
from Crypto import Random

from pgweb.mailqueue.util import send_simple_mail
from pgweb.util.helpers import template_to_string
import re

def send_template_mail(sender, receiver, subject, templatename, templateattr={}, usergenerated=False, cc=None):
	send_simple_mail(sender, receiver, subject,
					 template_to_string(templatename, templateattr),
					 usergenerated=usergenerated, cc=cc)

def get_client_ip(request):
	"""
	Get the IP of the client. If the client is served through our Varnish caches,
	or behind one of our SSL proxies, make sure to get the *actual* client IP,
	and not the IP of the cache/proxy.
	"""
	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
		# There is a x-forwarded-for header, so trust it but only if the actual connection
		# is coming in from one of our frontends.
		if request.META['REMOTE_ADDR'] in settings.FRONTEND_SERVERS:
			return request.META['HTTP_X_FORWARDED_FOR']

	# Else fall back and return the actual IP of the connection
	return request.META['REMOTE_ADDR']


def varnish_purge(url):
	"""
	Purge the specified URL from Varnish. Will add initial anchor to the URL,
	but no trailing one, so by default a wildcard match is done.
	"""
	url = '^%s' % url
	connection.cursor().execute("SELECT varnish_purge(%s)", (url, ))

def version_sort(l):
	"""
	map a directory name to a format that will show up sensibly in an ascii sort
	We specifically detect entries that look like versions. Weird things may happen
	if there is a mix of versions and non-versions in the same directory, but we
	generally don't have that.
	"""
	mkey = l['link']
	m = re.match('v?([0-9]+)\.([0-9]+)\.([0-9]+)$',l['url'])
	if m:
		mkey = m.group(1) + '%02d' % int(m.group(2)) + '%02d' % int(m.group(3));
	m = re.match('v?([0-9]+)\.([0-9]+)$',l['url'])
	if m:
		mkey = m.group(1) + '%02d' % int(m.group(2));
		# SOOO ugly. But if it's v10 and up, just prefix it to get it higher
		if int(m.group(1)) >= 10:
			mkey = 'a' + mkey
	m = re.match('v?([0-9]+)$', l['url'])
	if m:
		# This can only happen on 10+, so...
		mkey = 'a' + m.group(1) + '0'

	return mkey

def generate_random_token():
	"""
	Generate a random token of 64 characters. This token will be
	generated using a strong random number, and then hex encoded to make
	sure all characters are safe to put in emails and URLs.
	"""
	s = SHA256.new()
	r = Random.new()
	s.update(r.read(250))
	return s.hexdigest()
