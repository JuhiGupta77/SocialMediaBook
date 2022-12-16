from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account_settings', views.account_settings, name='account_settings'),
    path('upload', views.upload, name='upload'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]