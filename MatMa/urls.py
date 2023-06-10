from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('get', views.getData),
    path('add', views.postData, name='add'),
    path('', views.log, name='log'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('signin/', auth_view.LoginView.as_view(template_name='signin.html'), name='signin'),
    path('signout/', auth_view.LogoutView.as_view(template_name='signout.html'), name='signout'),
    path('search/', views.search, name='search'),
    path('adduser/', views.adduser, name='adduser'),
    path('edit_user/<str:pk>', views.edit_user, name='edit_user'),
    path('delete_user/<str:pk>', views.delete_user, name='delete_user'),
    path('user/', views.user, name='user'),
]