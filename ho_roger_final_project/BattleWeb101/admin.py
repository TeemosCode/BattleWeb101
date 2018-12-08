from django.contrib import admin

# Register your models here.
from .models import Player, Grid

admin.site.register(Player)
admin.site.register(Grid)