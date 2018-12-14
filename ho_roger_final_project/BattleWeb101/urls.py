from django.urls import path

from BattleWeb101.views import (
    Home,
    RandomSearchForOpponent,
    RenewEverydayData,

)

urlpatterns = [
    path('home/', Home.as_view(), name='home_urlpattern'),
    path('random_search_opponent/', RandomSearchForOpponent.as_view(), name="search_opponent"),
    path('daily_update/', RenewEverydayData.as_view()),
]
