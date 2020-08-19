from rest_framework import serializers
from .models import Profile, Projects

class ProfileSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'prof_photo')

class ProjectsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ('project', 'project_description', 'for_profile', 'repository_link', 'pub_date')