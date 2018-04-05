from django import forms

class DocCommentForm(forms.Form):
	name = forms.CharField(
		label='Your Name',
		max_length=100,
		required=True)
	email = forms.EmailField(
		label='Your Email',
		max_length=100,
		required=True)
	shortdesc = forms.CharField(
		max_length=100,
		required=True,
		label="Subject",)
	details = forms.CharField(
		label='Please explain why you are commenting on this page',
		required=True,
		widget=forms.Textarea)
