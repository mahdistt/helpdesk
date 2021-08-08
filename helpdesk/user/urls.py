from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='create-user'),
    path('login/', views.LoginView.as_view(), name='login-user'),
    path('logout/', views.LogoutView.as_view(), name='logout-user'),
]
