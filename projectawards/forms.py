from django import forms
from .models import Profile, Projects

class ProfileForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:', max_length=30)
    last_name = forms.CharField(label = 'Last Name:', max_length=30, required=False)
    bio = forms.CharField(label = "About You:", widget=forms.Textarea)
    phone_number = forms.IntegerField(label = "Phone Number:")
    profile_photo = forms.ImageField(label = "Profile Photo:")

class ProjectsForm(forms.Form):
    project = forms.CharField(label = 'Project Name:', max_length=50)
    description = forms.CharField(label = 'Project Description:', widget=forms.Textarea)
    repo = forms.CharField(label = 'Repository Link:', max_length=500)

class CommentForm(forms.Form):
    comment = forms.CharField(label = 'Comments:', max_length=2000)