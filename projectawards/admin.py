from django.contrib import admin

# Register your models here.
from .models import Profile, Projects, Comments, Review, Followers


admin.site.register(Profile)
admin.site.register(Projects)
admin.site.register(Followers)
admin.site.register(Comments)
admin.site.register(Review)