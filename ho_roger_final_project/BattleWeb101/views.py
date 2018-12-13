from django.shortcuts import render, get_object_or_404, redirect
# Used for class based views
from django.views import View

from .models import (
    Player,
    Grid,
    AttackedHistory,
)


##### Under development for Hardcoded player for testing ####

"""
PlayerName = Teemo
ID = 1
"""

class Home(View):

    def get(self, request):
        return render(request, 'battleweb101/home.html')




