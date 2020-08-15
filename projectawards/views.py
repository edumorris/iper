from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Image, Profile
from django.contrib.auth.decorators import login_required
# from .forms import ProfileForm, ImageUploadForm

# from .email import send_welcome_email

# Create your views here.
def index_test(request):
    title = "ingram index page testpage"

    return render(request, 'index.html', {"title": title})

def home(request):
    pass
