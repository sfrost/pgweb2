from django.utils.functional import SimpleLazyObject
from django.shortcuts import render
from django.conf import settings

# This is the whole site navigation structure. Stick in a smarter file?
sitenav = {
	'about': [
		{'title': 'About',              'link':'/about/'},
		{'title': 'Feature Matrix',     'link':'/about/featurematrix/'},
		{'title': 'Donate',             'link':'/about/donate/'},
		{'title': 'History',            'link':'/docs/current/static/history.html'},
		{'title': 'Sponsors',           'link':'/about/sponsors/', 'submenu': [
			{'title': 'Servers',    'link': '/about/servers/'},
		]},
		{'title': 'Latest news',        'link':'/about/newsarchive/'},
		{'title': 'Upcoming events',    'link':'/about/events/'},
		{'title': 'Press',              'link':'/about/press/'},
		{'title': 'Licence',            'link':'/about/licence/'},
	],
	'download': [
		{'title': 'Downloads',          'link':'/download/', 'submenu': [
				{'title': 'Binary',		'link':'/download/'},
				{'title': 'Source',		'link':'/ftp/source/'}
		]},
		{'title': 'Software Catalogue', 'link':'/download/product-categories/'},
		{'title': 'File Browser',       'link':'/ftp/'},
	],
	'docs': [
		{'title': 'Documentation',      'link':'/docs/'},
		{'title': 'Manuals',            'link':'/docs/manuals/', 'submenu': [
			{'title': 'Archive',    'link':'/docs/manuals/archive/'},
			{'title': 'French',     'link':'https://docs.postgresql.fr/'},
			{'title': 'Japanese',   'link':'http://www.postgresql.jp/document/'},
			{'title': 'Russian',    'link':'https://postgrespro.ru/docs/postgresql'},
		]},
		{'title': 'Books',              'link':'/docs/books/'},
		{'title': 'Online Resources',   'link':'/docs/online-resources/'},
		{'title': 'Wiki',               'link':'https://wiki.postgresql.org'},
	],
	'community': [
		{'title': 'Community',          'link':'/community/'},
		{'title': 'Contributors',       'link':'/community/contributors/'},
		{'title': 'Mailing Lists',      'link':'/list/'},
		{'title': 'IRC',                'link':'/community/irc/'},
        {'title': 'Slack',              'link':'https://postgres-slack.herokuapp.com/'},
		{'title': 'Local User Groups',  'link':'/community/user-groups/'},
        {'title': 'Events',             'link':'/about/events/'},
		{'title': 'International Sites','link':'/community/international/'},
	],
	'developer': [
		{'title': 'Developers',         'link':'/developer/'},
		{'title': 'Core Team',          'link':'/developer/core/'},
		{'title': 'Roadmap',            'link':'/developer/roadmap/'},
		{'title': 'Coding',             'link':'/developer/coding/'},
		{'title': 'Testing',            'link':'/developer/testing/', 'submenu': [
			{'title': 'Beta Information',  'link':'/developer/beta/'},
		]},
		{'title': 'Mailing Lists',      'link':'/list/'},
		{'title': 'Developer FAQ',      'link':'https://wiki.postgresql.org/wiki/Developer_FAQ'},
	],
	'support': [
		{'title': 'Support',            'link':'/support/'},
		{'title': 'Versioning policy',  'link':'/support/versioning/'},
		{'title': 'Security',           'link':'/support/security/'},
		{'title': 'Professional Services','link':'/support/professional_support/'},
		{'title': 'Report a Bug',       'link':'/account/submitbug/'},
	],
	'account': [
		{'title': 'Your account',         'link':'/account'},
		{'title': 'Profile',            'link':'/account/profile'},
		{'title': 'Submitted data',          'link':'/account', 'submenu': [
			{'title': 'News Articles',  'link':'/account/edit/news/'},
			{'title': 'Events',         'link':'/account/edit/events/'},
			{'title': 'Products',       'link':'/account/edit/products/'},
			{'title': 'Professional Services', 'link':'/account/edit/services/'},
			{'title': 'Organisations',  'link':'/account/edit/organisations/'},
		]},
		{'title': 'Change password',    'link':'/account/changepwd/'},
		{'title': 'Logout',             'link':'/account/logout'},
	],
}


def get_nav_menu(section):
	if sitenav.has_key(section):
		return sitenav[section]
	else:
		return {}

def render_pgweb(request, section, template, context):
	context['navmenu'] = get_nav_menu(section)
	return render(request, template, context)

def _get_gitrev():
	# Return the current git revision, that is used for
	# cache-busting URLs.
	try:
		with open('.git/refs/heads/master') as f:
			return f.readline()[:8]
	except IOError:
		# A "git gc" will remove the ref and replace it with a packed-refs.
		try:
			with open('.git/packed-refs') as f:
				for l in f.readlines():
					if l.endswith("refs/heads/master\n"):
						return l[:8]
				# Not found in packed-refs. Meh, just make one up.
				return 'ffffffff'
		except IOError:
			# If packed-refs also can't be read, just give up
			return 'eeeeeeee'

# Template context processor to add information about the root link and
# the current git revision. git revision is returned as a lazy object so
# we don't spend effort trying to load it if we don't need it (though
# all general pages will need it since it's used to render the css urls)
def PGWebContextProcessor(request):
	gitrev = SimpleLazyObject(_get_gitrev)
	if request.is_secure():
		return {
			'link_root': settings.SITE_ROOT,
			'gitrev': gitrev,
		}
	else:
		return {
			'gitrev': gitrev,
		}
