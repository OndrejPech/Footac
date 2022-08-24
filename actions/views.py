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
def team_actions_view(request, team_id):
    try:
        club = request.user.account.club
    except ObjectDoesNotExist:  # No club associated with user,
        return render(request, template_name='actions/no_club_account.html')

    club_teams_id = list(club.teams.all().values_list('id', flat=True))
    if team_id not in club_teams_id:  # user is not allowed to see this team
        return render(request, template_name='actions/restricted_access.html')

    team = get_object_or_404(Team, id=team_id)

    actions = Action.objects.filter(Q(team=team_id)| Q(opp_team=team_id))
    action_filter = ActionFilter(request.GET, queryset=actions, team_id=team_id)

    content = {'team': team, 'action_filter': action_filter}
    return render(request, template_name='actions/team_actions.html',
                  context=content)
