from django import forms
from django.forms import ValidationError

from pgweb.core.models import Organisation
from models import NewsArticle, NewsTag

class NewsArticleForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NewsArticleForm, self).__init__(*args, **kwargs)
	def filter_by_user(self, user):
		self.fields['org'].queryset = Organisation.objects.filter(managers=user, approved=True)
	def clean_date(self):
		if self.instance.pk and self.instance.approved:
			if self.cleaned_data['date'] != self.instance.date:
				raise ValidationError("You cannot change the date on an article that has been approved")
		return self.cleaned_data['date']

	@property
	def described_checkboxes(self):
		return {
			'tags': [(t.id, t.description) for t in NewsTag.objects.all()]
		}

	class Meta:
		model = NewsArticle
		exclude = ('submitter', 'approved', 'tweeted')
		widgets = {
			'tags': forms.CheckboxSelectMultiple,
		}
