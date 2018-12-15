from django.db import models
from django.db.models import F
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    # Limit players account name to length of 15 (would be enforced during signup)
    player_name = models.CharField(max_length=15)
    player_bullets = models.IntegerField(default=3)
    player_hit_points = models.IntegerField(default=20)
    player_suncker_points = models.IntegerField(default=0)
    player_total_shots = models.IntegerField(default=0)  # All historical shots the player has made since his first shot
    player_total_hits = models.IntegerField(default=0)  # Shots that actually hit
    player_accuracy = models.DecimalField(default=0.000, max_digits=6, decimal_places=3)  # 0.000 This field is COOL!!!

    def save(self):
        # Save the calculated derived data (This is the shitty part about Django ORM...) in a % floating point way
        # Add the "%" during the front end view display...

        # Avoid ZeroDivisionError: division by zero Error!
        if self.player_total_shots == 0:
            self.player_accuracy = 0.000
        else:
            self.player_accuracy = self.player_total_hits / self.player_total_shots

        super(Player, self).save()

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
        ordering = ['player', 'grid_x', 'grid_y']
        unique_together = (('player', 'grid_x', 'grid_y'),)


class AttackedHistory(models.Model):
    attacker = models.ForeignKey(Player, related_name='attacker', on_delete=models.PROTECT)
    victim = models.ForeignKey(Player, related_name='victim', on_delete=models.PROTECT)
    created_time = models.DateTimeField(auto_now_add=True)
    hit = models.BooleanField(default=False)
    grid_x_hit = models.IntegerField(null=True)
    grid_y_hit = models.IntegerField(null=True)

    def __str__(self):
        return "Attacker Info: %s  -  Victim Info: %s" % (self.attacker, self .victim)

    # This is uncommneted only when the version of the game no longer allows the same person to attack the same victim
    # within the same day...
    # class Meta:
    #     unique_together = (("attacker", "victim"),)


