from django.conf.urls import url 
from . import views


urlpatterns = [
    url(r'^get_users/$', views.get_all_users, name='get users'),
    url(r'^user/$', views.user_crud, name='user'),
]
