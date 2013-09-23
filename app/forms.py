from django import forms

class RegistrationForm(forms.Form):
	name = forms.CharField(required=True, max_length=100)
	email = forms.EmailField(required=True)
	phonenumber = forms.CharField(required=True, max_length= 12)

class LoginForm(forms.Form):
	phonenumber = forms.CharField(required=True, max_length=12)