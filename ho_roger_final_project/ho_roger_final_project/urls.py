"""ho_roger_final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URstaLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('',
         RedirectView.as_view(
             pattern_name='index_urlpattern',  # Sends to the /home page under the BattleWeb101 app at root url
             permanent=False
         )),

    path('login/',
         LoginView.as_view(template_name='battleweb101/login.html'),
         name='login_urlpattern'
         ),
    #
    path('logout/',
         LogoutView.as_view(),
         name='logout_urlpattern'
         ),


    path('admin/', admin.site.urls),
    # path('', include('BattleWeb101.urls', namespace='BattleWeb101')),
    path('', include('BattleWeb101.urls')),

    ## Authentication -- Email Password Reset !!! Django 2.0.1 Changed alot of this authentication stuff. Relook at this when Time permits!
    path('password_reset', PasswordResetView, name="password_reset"),
    path('password_reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/(P<uidb64>[0-9A-Za-z_\-]+)/(P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
