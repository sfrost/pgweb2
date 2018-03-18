from django.shortcuts import get_object_or_404
from django.http import Http404
from pgweb.util.decorators import login_required

from datetime import date

from pgweb.util.contexts import render_pgweb
from pgweb.util.helpers import simple_form

from models import Event
from forms import EventForm

def main(request):
	community_events = Event.objects.select_related('country').filter(approved=True, badged=True).filter(training=False, enddate__gt=date.today()).order_by('enddate', 'startdate',)
	other_events = Event.objects.select_related('country').filter(approved=True, badged=False).filter(training=False, enddate__gt=date.today()).order_by('enddate', 'startdate',)
	training = Event.objects.select_related('country').filter(approved=True).filter(training=True, enddate__gt=date.today()).order_by('enddate', 'startdate',)
	return render_pgweb(request, 'about', 'events/archive.html', {
		'title': 'Upcoming events',
		'eventblocks': (
			{ 'name': 'Community Events', 'events': community_events, 'link': '',},
			{ 'name': 'Other Events', 'events': other_events, 'link': '',},
			{ 'name': 'Training', 'events': training, 'link': 'training/',},
		),
	})

def _eventarchive(request, training, title):
	# Hardcode to the latest 100 events. Do we need paging too?
	events = Event.objects.select_related('country').filter(approved=True).filter(training=training, enddate__lte=date.today()).order_by('-enddate', '-startdate',)[:100]
	return render_pgweb(request, 'about', 'events/archive.html', {
			'title': '%s Archive' % title,
			'archive': True,
			'eventblocks': (
				{'name': title, 'events': events, },
				),
	})

def archive(request):
	return _eventarchive(request, False, 'Event')

def trainingarchive(request):
	return _eventarchive(request, True, 'Training')

def item(request, itemid, throwaway=None):
	event = get_object_or_404(Event, pk=itemid)
	if not event.approved:
		raise Http404
	return render_pgweb(request, 'about', 'events/item.html', {
		'obj': event,
	})

@login_required
def form(request, itemid):
	return simple_form(Event, itemid, request, EventForm,
					   redirect='/account/edit/events/')
