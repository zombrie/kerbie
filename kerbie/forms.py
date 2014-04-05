from django import forms
from kerbie.models import comment, post, search, userProfile, addImage
from django.contrib.auth.models import User
import datetime

class search_form(forms.ModelForm):
	name = forms.CharField()
	class Meta:
		model = search
		fields = ('name',)

class user_form(forms.ModelForm):
	username = forms.CharField(help_text="Please enter a username.")
	email = forms.CharField(help_text="Please enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class user_profile_form(forms.ModelForm):
	birthday = forms.DateField(initial=datetime.date.today,help_text="Please enter your birthday.")
	location = forms.CharField(help_text="Please enter your location.")
	gender = forms.CharField(help_text="Please enter your gender: m/f.")
	class Meta:
		model = userProfile
		fields = ('location', 'birthday', 'gender')

class addImage_form(forms.ModelForm):
	image = forms.ImageField(label='Select image to upload')
	class Meta:
		model = addImage
		fields=('image', 'title')
		
class post_form(forms.ModelForm):
	postBody = forms.CharField(widget=forms.Textarea, max_length=200)
	class Meta:
		model = post
		fields= ('postBody',)
		
class comment_form(forms.ModelForm):
	commentBody = forms.CharField(widget=forms.Textarea, max_length=200)
	class Meta:
		model = comment
		fields = ('commentBody',)
		
class profile_picture_form(forms.ModelForm):
	class Meta:
		model = addImage