from django.conf.urls import url 
from . import views


urlpatterns = [
    url(r'^radius/$', views.get_radius, name='get radius'),
    url(r'^login/$', views.login, name='login'),
    url(r'^get_users/$', views.get_all_users, name='get users'),
    url(r'^user/$', views.user_crud, name='user'),
]
