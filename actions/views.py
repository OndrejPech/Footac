from django.shortcuts import render, get_object_or_404
from actions.models import Club,Team, Player, League, Game, Action
from .filters import ActionFilter
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def home_view(request):
    content = {}
    return render(request, template_name='actions/homepage.html', context=content)


@login_required
def club_view(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    teams = club.teams.all()
    id_s = [team.id for team in teams]  # all team_ids in club
    # all games where club team anticipate TODO need to check woth more data
    games = Game.objects.filter(Q(home_team_id__in=id_s) | Q(away_team_id__in=id_s))
    players = club.players.all()
    content = {'club': club, 'teams': teams, 'players': players, 'games': games}
    return render(request, template_name='actions/club_detail.html',
                  context=content)


@login_required
def club_actions_view(request):
    try:
        club = request.user.account.club
    except ObjectDoesNotExist:  # No club associated with user,
        return render(request, template_name='actions/no_club_account.html')

    # TODO
    teams = club.teams.all()
    id_s = [team.id for team in teams]  # all team_ids in club
    actions = Action.objects.filter(Q(team=id_s[2])| Q(opp_team=id_s[2])) # TODO
    action_filter = ActionFilter(request.GET, queryset=actions)

    content = {'club': club, 'action_filter': action_filter}
    return render(request, template_name='actions/action.html',
                  context=content)


# JUST FOR PRACTICE
@login_required()
def list_games_view(request):
    club_id = request.user.account.club_id
    club = get_object_or_404(Club, id=club_id)
    teams = club.teams.all()

    if request.method == 'POST':
        content = {'club': club, 'teams': teams}
        return render(request, template_name='actions/games.html', context=content)

    team = teams[2]
    games = Game.objects.filter(home_team=team.id)
    content = {'club': club, 'teams': teams, 'team': team, 'games': games}
    return render(request, template_name='actions/games.html', context=content)


