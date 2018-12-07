from django.db import models
from django.urls import reverse


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_bullets = models.IntegerField()
    player_hit_points = models.IntegerField()
    player_suncker_points = models.IntegerField()
    pass


class Grid(models.Model):
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    pass


class HallOfFame(models.Model):
    pass


class HallOfSunckers(models.Model):
    pass
