from django import forms
from .models import Snippet

class SearchForm(forms.Form):
	Search = forms.CharField()

class SnippetForm(forms.ModelForm):
	Search = forms.CharField(widget = forms.TextInput(
		attrs={
		'class':"form-control", 'placeholder':"Профессия"
		}
		))
	class Meta:
		model = Snippet
		fields = ('Search',)