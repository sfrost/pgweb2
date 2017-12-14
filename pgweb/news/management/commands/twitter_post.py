#!/usr/bin/env python
#
# Script to post previosly unposted news to twitter
#
#

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.conf import settings

from datetime import datetime, timedelta
import time

from pgweb.news.models import NewsArticle

import requests_oauthlib

class Command(BaseCommand):
	help = 'Post to twitter'

	def handle(self, *args, **options):
		curs = connection.cursor()
		curs.execute("SELECT pg_try_advisory_lock(62387372)")
		if not curs.fetchall()[0][0]:
			raise CommandError("Failed to get advisory lock, existing twitter_post process stuck?")

		articles = list(NewsArticle.objects.filter(tweeted=False, approved=True, date__gt=datetime.now()-timedelta(days=7)).order_by('date'))
		if not len(articles):
			return

		tw = requests_oauthlib.OAuth1Session(settings.TWITTER_CLIENT,
											 settings.TWITTER_CLIENTSECRET,
											 settings.TWITTER_TOKEN,
											 settings.TWITTER_TOKENSECRET)

		for a in articles:
			# We hardcode 30 chars for the URL shortener. And then 10 to cover the intro and spacing.
			statusstr = u"News: {0} {1}/about/news/{2}/".format(a.title[:140-40], settings.SITE_ROOT, a.id)
			r = tw.post('https://api.twitter.com/1.1/statuses/update.json', data={
				'status': statusstr,
			})
			if r.status_code != 200:
				print("Failed to post to twitter: %s " % r)
			else:
				a.tweeted = True
				a.save()
			# Don't post more often than once / 30 seconds, to not trigger flooding.
			time.sleep(30)
