from django.urls import path

from bases.views import Home, HomesinPrivilegios

# importar para las vistas de login

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bases/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bases/login.html'), name='logout'),

    path('sin_privilegios/', HomesinPrivilegios.as_view(), name='sin_privilegios'),

]