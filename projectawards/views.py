from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Profile, Projects
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProjectsForm

# RestAPI Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectsSerializers, ProfileSerializers
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# from .email import send_welcome_email

# Create your views here.
def index_test(request):
    title = "Iper testpage"

    return render(request, 'index.html', {"title": title})
    
@login_required(login_url='/accounts/login')
def home(request):
    current_user = request.user
    profile = Profile.objects.get(user = current_user.id)

    current_user = request.user
    title = "Home"

    return render(request, 'home.html', {"current_user": current_user, "profile": profile, "title": title})

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    
    current_user = request.user
    my_projects = Projects.objects.filter(project_owner = user_id).order_by('-id')
    
    profile = Profile.objects.get(user = user_id)
    return render(request, 'profile.html', {"current_user": current_user, "profile": profile, "projects": my_projects})

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

@login_required(login_url='/accounts/login')
def project_upload(request, user_id):
    prof_user = Profile.objects.get(user=user_id)
    
    title = "Project Upload"
    profile = Profile.objects.get(user = user_id)

    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['project']
            project_description = form.cleaned_data['description']
            project_repo = form.cleaned_data['repo']

            new_project = Projects(project = project_name, project_description = project_description, repository_link = project_repo, project_owner = prof_user)
            new_project.save_project()

            return redirect(home)
    else:
        form = ProjectsForm()
    
    return render(request, 'project_upload.html', {"title": title, "ProjectUploadForm": form, "profile": profile})

# API Functionality
class ProjectsList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAdminOrReadOnly)
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializers(all_projects, many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        permission_classes = (IsAdminOrReadOnly)
        serializers = ProjectsSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAdminOrReadOnly)
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializers(all_profiles, many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        permission_classes = (IsAdminOrReadOnly)
        serializers = ProfileSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)