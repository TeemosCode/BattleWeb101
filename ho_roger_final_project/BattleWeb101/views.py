from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# Used for class based views
from django.views import View
import random, itertools
# For User creation and Signup with email confirmation
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from BattleWeb101.tokens import account_activation_token
from .forms import SignUpForm, UserInfoForm
# from mysite.core.tokens import account_activation_token

from .models import (
    Player,
    Grid,
    AttackedHistory,
)


def sign_up(request):

    # Would still need to implement and handle "UserName Already Used" situations in the future!!!
    form = UserInfoForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        username = form.cleaned_data['username']
        user.username = username
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate Your BattleWeb101 Account'
        message = render_to_string('battleweb101/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(mail_subject, message) # Sends email to the provided email from the user
        # username = form.cleaned_data['username']
        # to_email = username + '@illinois.edu'  # Illinois mail combining username (NetID) with '@illinois.edu'
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        # return render(request, 'battleweb101/account_activation_email.html')
        print("Signed Up with email: " + user.email)
        return HttpResponse("Please go to your provided email to activate your BattleWeb101 account!")
        # return HttpResponseRedirect('/home')
    else:
        form = UserInfoForm()

    context = {'form': form}
    return render(request, 'battleweb101/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as error:
        print(error)
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        ## Save the User information into Player table
        player = Player()
        player.player_name = user.username
        player.save()
        # Log the user into the system.
        # Immediately log in user and send them to the home page
        login(request, user)
        return render(request, 'battleweb101/home.html')
    else:
        return HttpResponse('Activation link is invalid!')


class Index(View):

    def get(self, request):
        return render(request, 'battleweb101/root.html')


class Home(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'battleweb101/home.html')


class RandomSearchForOpponent(LoginRequiredMixin, View):
    grid_upper_limit = 10
    grid_lower_limit = 0

    def get(self, request):
        # Hard code during initial development to exclude the player him/ herself, don't want players hitting themselves
        self_excluded_player_query_list = Player.objects.exclude(player_name=request.user.username)

        player_self = Player.objects.get(player_name=request.user.username)
        # .... Are there any better ways???
        # Making sure not to find a player that has already been sunk. (No more grids within the grid table for him/her)
        player_query_list = []
        for player in self_excluded_player_query_list:
            # Only get players who have not been totally sunk! (Still his grid values for the day)
            if Grid.objects.filter(player__player_name=player.player_name).count() != 0:
                player_query_list.append(player)

        rand_index = random.randint(0, len(player_query_list) - 1)
        opponent = player_query_list[rand_index]
        number_range = range(self.grid_lower_limit, self.grid_upper_limit)
        context = {
            "opponent": opponent,
            'number_range': number_range,
            'player': player_self
        }

        return render(request, 'battleweb101/opponent.html', context=context)

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
        # Reset these two fields back to their defaults <-- Great design here!
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
                grid = Grid(player=player, grid_x=x, grid_y=y)
                grid.save()

    def get(self, request):
        self.renew_player_daily_data()
        self.renew_grid_data()
        return HttpResponse("Daily data for update updated within the database successfully!")


class HallOfSunckers(View):
    number_of_sunckers_to_display = 10

    def get(self, request):
        suncker_player_list_descending_order = Player.objects.all().exclude(player_suncker_points=0).\
            order_by('-player_suncker_points')
        context = {
            # Get the top N of sunckers
            'suncker_player_list': suncker_player_list_descending_order[:self.number_of_sunckers_to_display]
        }
        return render(request, 'battleweb101/hallOfSUnCKERS.html', context=context)


class HallOfFame(View):
    number_of_fames_to_display = 10

    def get(self, request):
        list_of_fames_descending_order = Player.objects.all().exclude(player_accuracy=0.000).order_by('-player_accuracy')
        context = {
            'hall_of_fame_list': list_of_fames_descending_order
        }
        return render(request, 'battleweb101/HallOfFame.html', context=context)


class ViewAttackedHistory(LoginRequiredMixin, View):
    """
    This view is associated with each individual player
    """
    def get(self, request):
        
        player_self_object = Player.objects.get(player_name=request.user.username)

        list_of_attacks = AttackedHistory.objects.filter(victim=player_self_object).order_by('-created_time')
        context = {
            'list_of_attacks': list_of_attacks
        }
        return render(request, 'battleweb101/attacked_history.html', context=context)


class Attack(LoginRequiredMixin, View):
    """
    Should contain only a POST method
    Used to attack a random searched user.
    Yet because it is still currently under development, we will hard code the target ID and attacker first, as well
    as the grid_x and grid_y coordinates.
    Would need to add any activity to the Attack History!

    In order to hide the attack information from users, I will not use pass the variables from the templates to the
    views with the url links as users could follow a certain pattern to attack others. Instead, I will embed the
    information into a form and use POST to handle it instead. --> request.POST.get('name variable')
    """
    # It should be POST...
    def post(self, request):

        # Victim - accessed through request.POST.get('victim')   name = "victim" in the form
        victim_name = request.POST.get('victim')
        victim = Player.objects.get(player_name=victim_name)
        # The attacker of the request
        attacker = Player.objects.get(player_name=request.user.username)

        # Attacker has no more bullets to shoot...
        if attacker.player_bullets == 0:
            print(attacker.player_name + " Has no more bullets left!")
            #### This part should add some more cool business logic. Not just go boom!!!
            return render(request, 'battleweb101/home.html')

        hit = True
        attacker.player_total_shots += 1
        attacker.player_bullets -= 1

        current_attack_history = AttackedHistory()

        # Hard coded coordinates for attack
        x = request.POST.get('x')
        y = request.POST.get('y')

        # Check if hit
        attacked_result = Grid.objects.filter(player=victim, grid_x=x, grid_y=y)
        # If length is 0, it means it hit nothing (The victim does not have that grid_x & grid_y)
        if len(attacked_result) == 0:
            hit = False
        else: # HIT!!!

            attacker.player_total_hits += 1
            victim.player_hit_points -= 1
            current_attack_history.grid_x_hit = x
            current_attack_history.grid_y_hit = y
            current_attack_history.hit = True

            # Delete the hit grid of the victim
            Grid.objects.filter(player=victim, grid_x=x, grid_y=y).delete()

            # Check if victim is sunck...
            if victim.player_hit_points == 0:
                victim.player_suncker_points += 1
                # There could also be a SuNCKER KING UPDATE HERE lol...

        current_attack_history.victim = victim
        current_attack_history.attacker = attacker
        current_attack_history.save()
        attacker.save()
        victim.save()

        context = {
            'hit': hit,
            'x': x,
            'y': y,
            'victim': victim,
            'attacker': attacker,
        }

        return render(request, 'battleweb101/attack_result.html', context=context)


class PlayerStatus(LoginRequiredMixin, View):

    def get(self, request):
        player = Player.objects.get(player_name=request.user.username)
        context = {
            'player': player
        }
        return render(request, 'battleweb101/player_status.html', context=context)


class UI(View):

    def get(self,request):
        print(request.user.username)
        return render(request, 'battleweb101/root.html')
