from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	full_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = User
		fields = ('username', 'full_name', 'phone', 'address', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
  
  
class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 7}))
