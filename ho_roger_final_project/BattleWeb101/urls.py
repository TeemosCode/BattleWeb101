from django.urls import path
from django.conf.urls import url

from BattleWeb101.views import (
    Home,
    RandomSearchForOpponent,
    RenewEverydayData,
    HallOfSunckers,
    HallOfFame,
    ViewAttackedHistory,
    Attack,
    PlayerStatus,

    sign_up,
    activate,
)

# app_name = 'BattleWeb101'

urlpatterns = [
    path('home/', Home.as_view(), name='home_urlpattern'),
    path('random_search_opponent/', RandomSearchForOpponent.as_view(), name="search_opponent_urlpattern"),
    path('daily_update/', RenewEverydayData.as_view()),
    path('Hall_Of_SUnCKERS/', HallOfSunckers.as_view(), name='hall_of_sunckers_urlpattern'),
    path('hall_of_fame/', HallOfFame.as_view(), name='hall_of_fame_urlpattern'),
    path('attacked_history/', ViewAttackedHistory.as_view(), name='attack_history_urlpattern'),
    path('attack/', Attack.as_view(), name='attack_urlpattern'),
    path('status/', PlayerStatus.as_view(), name='player_status_urlpattern'),

    path('signup/', sign_up, name='signup_urlpattern'),
    # path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #      views.activate, name='activate'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
