from django import forms

class RegistrationForm(forms.Form):
	fornavn = forms.CharField(required=True, max_length=20)
	etternavn = forms.CharField(required=True, max_length=20)
	epost = forms.EmailField(required=True)

class LoginForm(forms.Form):
	epost = forms.EmailField(required=True)