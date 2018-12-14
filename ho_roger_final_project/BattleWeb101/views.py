from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# Used for class based views
from django.views import View
import random, itertools
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


class RandomSearchForOpponent(View):

    def get(self, request):
        # Hard code during initial development to exclude the player him/ herself, don't want players hitting themselves
        self_excluded_player_query_list = Player.objects.exclude(player_name='Teemo').exclude()
        # .... Are there any better ways???
        # Making sure not to find a player that has already been sunk. (No more grids within the grid table for him/her)
        player_query_list = []
        for player in self_excluded_player_query_list:
            if Grid.objects.filter(player__player_name=player.player_name).count() != 0:
                player_query_list.append(player)

        rand_index = random.randint(0, len(player_query_list) - 1)
        opponent = player_query_list[rand_index]

        return render(request, 'battleweb101/opponent.html', context={"opponent": opponent})

# Accessing all grid data for a certain player through foreign key | BELOW
# Grid.objects.filter(player__player_name='Shroom')


class RenewEverydayData(View):

    # variable for the start and end index number of the grids (Could be changed in the future.
    # This is a more flexible design)
    grid_upper_limit = 10
    grid_lower_limit = 0
    total_grid_number = 20

    def find_all_players(self):
        player_instances = Player.objects.all()
        return player_instances

    def renew_player_daily_data(self):
        player_daily_bullets = Player._meta.get_field('player_bullets').get_default()
        player_daily_hit_points = Player._meta.get_field('player_hit_points').get_default()
        player_instance_list = self.find_all_players()

        # loop through all instances of the players, update those two daily values and save it to database for update
        for player in player_instance_list:
            player.player_bullets = player_daily_bullets
            player.player_hit_points = player_daily_hit_points
            player.save()

    def renew_grid_data(self):
        player_instance_list = self.find_all_players()

        # Bulk Delete the Grid table data entries
        Grid.objects.all().delete()

        # Repopulate Grid table with random 20 grid x,y for each player
        for player in player_instance_list:
            # Generate random combinations of x,y within the range of 0 ~ 10
            grid_x_y_combination_list = list(
                itertools.combinations([num for num in range(self.grid_lower_limit, self.grid_upper_limit)], 2)
            )
            # Randomly shuffle them then get the front n elements of the list for the n grids for different players
            random.shuffle(grid_x_y_combination_list)
            list_with_total_grid_number_coordinates = grid_x_y_combination_list[:self.total_grid_number]
            # loop through the generated x,y pair to insert into the Grid table for the player
            for x, y in list_with_total_grid_number_coordinates:
                grid = Grid(player=player, grid_x=x, grid_y = y)
                grid.save()

    def get(self, request):
        self.renew_player_daily_data()
        self.renew_grid_data()
        return HttpResponse("Daily data for update updated within the database successfully!")




