from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Profile, Projects
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

# from .email import send_welcome_email

# Create your views here.
def index_test(request):
    title = "Iper testpage"

    return render(request, 'index.html', {"title": title})

def home(request):
    latest_projects = Projects.objects.order_by('-id').select_related('profile').all()
    current_user = request.user
    profile = Profile.objects.get(user = current_user.id)

    current_user = request.user

    return render(request, 'home.html', {"latest_pics": latest_pics, "current_user": current_user, "profile": profile})

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    
    current_user = request.user
    imgs = Image.objects.filter(profile = current_user.id)
    profile = Profile.objects.get(user = user_id)
    return render(request, 'profile.html', {"current_user": current_user, "imgs": imgs, "profile": profile})

@login_required(login_url='/accounts/login')
def profile_update(request, user_id):

    title = 'Update Profile'
    profile = Profile.objects.get(user = user_id)

    current_user = request.user

    email = current_user.email

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            about = form.cleaned_data['bio']
            mobile = form.cleaned_data['phone_number']
            dp = form.cleaned_data['profile_photo']
            
            Profile.objects.filter(user = request.user).update(first_name = fname, last_name = lname, email = current_user.email, bio = about, phone_number = mobile, prof_photo = dp)

            return redirect(home)

    else:
        form = ProfileForm()
    
    return render(request, 'profile_update.html', {"ProfileForm": form, "title": title, "profile": profile})
