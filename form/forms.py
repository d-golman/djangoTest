from django import forms


class SearchForm(forms.Form):
	Search = forms.CharField()