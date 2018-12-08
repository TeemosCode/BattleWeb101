from django.db import models
from django.urls import reverse


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    # Limit players account name to length of 15 (would be enforced during signup)
    player_name = models.CharField(max_length=15)
    player_bullets = models.IntegerField(default=3)
    player_hit_points = models.IntegerField(default=20)
    player_suncker_points = models.IntegerField(default=0)

    def __str__(self):
        return "Name: %s. ID: %s" % (self.player_name, self.player_id)

    class Meta:
        ordering = ['player_id']


class Grid(models.Model):
    player = models.ForeignKey(Player, related_name='grid', on_delete=models.PROTECT)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    class Meta:
        ordering = ['grid_x', 'grid_y']

