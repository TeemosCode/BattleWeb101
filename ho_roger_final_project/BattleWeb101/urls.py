from django.urls import path

from BattleWeb101.views import (
    Home,
)

urlpatterns = [
    path('home/', Home.as_view(), name='home_urlpattern'),
]
