from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
	(r'^$', 'pgweb.account.views.home'),

	# Community authenticatoin
	(r'^auth/(\d+)/$', 'pgweb.account.views.communityauth'),
	(r'^auth/(\d+)/logout/$', 'pgweb.account.views.communityauth_logout'),
	(r'^auth/(\d+)/search/$', 'pgweb.account.views.communityauth_search'),
	(r'^auth/(\d+)/getkeys/(\d+/)?$', 'pgweb.account.views.communityauth_getkeys'),

	# Profile
	(r'^profile/$', 'pgweb.account.views.profile'),
	(r'^profile/change_email/$', 'pgweb.account.views.change_email'),
	(r'^profile/change_email/([0-9a-f]+)/$', 'pgweb.account.views.confirm_change_email'),

	# List of items to edit
	(r'^edit/(.*)/$', 'pgweb.account.views.listobjects'),

	# News & Events
	(r'^news/(.*)/$', 'pgweb.news.views.form'),
	(r'^events/(.*)/$', 'pgweb.events.views.form'),

	# Software catalogue
	(r'^organisations/(.*)/$', 'pgweb.core.views.organisationform'),
	(r'^products/(.*)/$', 'pgweb.downloads.views.productform'),

	# Organisation information
	(r'^orglist/$', 'pgweb.account.views.orglist'),

	# Professional services
	(r'^services/(.*)/$', 'pgweb.profserv.views.profservform'),

	# Docs comments
	(r'^comments/(new)/(.*)/(.*)/$', 'pgweb.docs.views.commentform'),

	# Log in, logout, change password etc
	(r'^login/$', 'pgweb.account.views.login'),
	(r'^logout/$', 'pgweb.account.views.logout'),
	(r'^changepwd/$', 'pgweb.account.views.changepwd'),
	(r'^changepwd/done/$', 'pgweb.account.views.change_done'),
	(r'^reset/$', 'pgweb.account.views.resetpwd'),
	(r'^reset/done/$', 'pgweb.account.views.reset_done'),
	(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'pgweb.account.views.reset_confirm'),
	(r'^reset/complete/$', 'pgweb.account.views.reset_complete'),
	(r'^signup/$', 'pgweb.account.views.signup'),
	(r'^signup/complete/$', 'pgweb.account.views.signup_complete'),
	(r'^signup/oauth/$', 'pgweb.account.views.signup_oauth'),
)

for provider in settings.OAUTH.keys():
	urlpatterns.append(url(r'^login/({0})/$'.format(provider), 'pgweb.account.oauthclient.login_oauth'))
