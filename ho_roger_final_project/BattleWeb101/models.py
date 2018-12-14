from django.db import models
from django.urls import reverse


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    # Limit players account name to length of 15 (would be enforced during signup)
    player_name = models.CharField(max_length=15)
    player_bullets = models.IntegerField(default=3)
    player_hit_points = models.IntegerField(default=20)
    player_suncker_points = models.IntegerField(default=0)
    player_total_shots = models.IntegerField(default=0)  # All historical shots the player has made since his first shot
    player_total_hits = models.IntegerField(default=0)  # Shots that actually hit

    def __str__(self):
        return "Name: %s. ID: %s" % (self.player_name, self.player_id)

    class Meta:
        ordering = ['player_id']


class Grid(models.Model):
    player = models.ForeignKey(Player, related_name='grid', on_delete=models.PROTECT)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    def __str__(self):
        return "Player: %s,  Player_ID: %s   (grid_x: %s, grid_y: %s)" \
               % (self.player.player_name, self.player.player_id, self.grid_x, self.grid_y)

    class Meta:
        ordering = ['grid_x', 'grid_y']
        unique_together = (('player', 'grid_x', 'grid_y'),)


class AttackedHistory(models.Model):
    attacker_id = models.ForeignKey(Player, related_name='attacker', on_delete=models.PROTECT)
    victim_id = models.ForeignKey(Player, related_name='victim', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "AttackerID: %s  -  VictimID: %s" % (self.attacker_id, self .victim_id)

    class Meta:
        unique_together = (("attacker_id", "victim_id"),)

