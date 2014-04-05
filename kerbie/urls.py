from django.conf.urls import patterns, include, url
from kerbie import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', views.search, name='search'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^user_profile/', views.user_profile, name='user_profile'),
    url(r'^matches/$', views.search_matches, name='search_matches'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^pictures/', views.pictures, name='user_pictures'),
    url(r'^add_pictures/', views.add_pictures, name='add_pictures'),
    url(r'^comments/(\d{1,2})/', views.comments, name='comments'),
) 


