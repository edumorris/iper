from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Profile, Projects, Comments, Review
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProjectsForm, CommentForm, ReviewForm

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
    projects = Projects.objects.order_by('-id').all().select_related('project_owner')

    current_user = request.user
    title = "Home"

    return render(request, 'home.html', {"current_user": current_user, "profile": profile, "title": title, "projects": projects})

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

@login_required(login_url='/accounts/login')
def commenting(request, project_id, user_id):
    current_user = request.user
    title = "Comments"

    profile = Profile.objects.get(user = user_id)
    project = Projects.objects.get(id = project_id)

    old_comments = Comments.objects.filter(for_project = project_id).all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.cleaned_data['comment']

            add_comment = Comments(for_project = project, comment = new_comment, submitted_by = profile)
            add_comment.save()

            return redirect(home)
    else:
        form = CommentForm()
    
    return render(request, 'comments.html', {"title": title, "CommentForm": form, "project": project, "old_comments": old_comments, "profile": profile})

@login_required(login_url='/accounts/login')
def reviewing(request, project_id, user_id):
    current_user = request.user
    title = "Review"

    profile = Profile.objects.get(user = user_id)
    project = Projects.objects.get(id = project_id)

    old_comments = Comments.objects.filter(for_project = project_id).all()
    old_reviews = Review.objects.filter(for_project = project_id).all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            ui = form.cleaned_data['ui']
            ux = form.cleaned_data['ux']
            screen_reponse = form.cleaned_data['screens']
            functions = form.cleaned_data['functions']
            input_output = form.cleaned_data['io']
            content = form.cleaned_data['content']

            des_av = ("%.2f" % ((ui+ux+screen_reponse)/3))
            usability_av = ("%.2f" % ((functions+input_output)/2))
            total = ("%.2f" % ((float(des_av)+float(usability_av)+content)/3))

            add_review = Review(for_project = project, submitted_by = profile, user_interface = ui, user_experience = ux, responsiveness = screen_reponse, design_average = float(des_av), functionality = functions, io = input_output, usability_average = float(usability_av), content_average = content, total_average = float(total))
            add_review.save()

            return redirect(home)
    else:
        form = ReviewForm()
    
    return render(request, 'review.html', {"title": title, "ReviewForm": form, "project": project, "old_reviews": old_reviews, "profile": profile})



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