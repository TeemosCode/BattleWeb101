from django.urls import path

from BattleWeb101.views import (
    Home,
    RandomSearchForOpponent,
    RenewEverydayData,
    HallOfSunckers,
    HallOfFame,

)

urlpatterns = [
    path('home/', Home.as_view(), name='home_urlpattern'),
    path('random_search_opponent/', RandomSearchForOpponent.as_view(), name="search_opponent_urlpattern"),
    path('daily_update/', RenewEverydayData.as_view()),
    path('Hall_Of_SUnCKERS/', HallOfSunckers.as_view(), name='hall_of_sunckers_urlpattern'),
    path('hall_of_fame/', HallOfFame.as_view(), name='hall_of_fame_urlpattern'),
]
