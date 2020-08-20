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

class ReviewForm(forms.Form):
    ui = forms.IntegerField(label = 'User Interface:', max_value=10, min_value=1)
    ux = forms.IntegerField(label = 'User Experience:', max_value=10, min_value=1)
    screens = forms.IntegerField(label = 'Screen Reponsiveness:', max_value=10, min_value=1)
    functions = forms.IntegerField(label = 'Project Functionality:', max_value=10, min_value=1)
    io = forms.IntegerField(label = 'Input/Output Accuracy:', max_value=10, min_value=1)
    content = forms.IntegerField(label = 'Content:', max_value=10, min_value=1)
    # total = forms.ChoiceField(choices=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
