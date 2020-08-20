from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name ='home'),
    url(r'^index/$', views.index_test, name='index'),
    url(r'^profile/(\d+)', views.profile, name='profile'),
    url(r'^profile_update/(\d+)', views.profile_update, name='profile_update'),
    url(r'^project_upload/(\d+)', views.project_upload, name='project_upload'),
    url(r'^comment/(\d+)/(\d+)', views.commenting, name='commenting'),
    url(r'^review/(\d+)/(\d+)', views.reviewing, name='reviewing'),
    # url(r'^like/(\d+)', views.likes, name='liking'),
    # APIs
    url(r'^api/projects/$', views.ProjectsList.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)