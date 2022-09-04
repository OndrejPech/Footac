from django.shortcuts import render, get_object_or_404, redirect
from actions.models import Club, Team, Player, League, Game, Action
from .filters import ActionFilter
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import ActionForm


def home_view(request):
    content = {}
    return render(request, template_name='actions/homepage.html', context=content)


@login_required
def club_view(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    teams = club.teams.all()
    id_s = [team.id for team in teams]  # all team_ids in club
    # all games where club team anticipate
    games = Game.objects.filter(Q(home_team_id__in=id_s) | Q(away_team_id__in=id_s))
    players = club.players.all()
    content = {'club': club, 'teams': teams, 'players': players, 'games': games}
    return render(request, template_name='actions/club_detail.html',
                  context=content)


@login_required
def team_actions_view(request, team_id):

    # CHECK USER ALLOWANCE
    try:
        club = request.user.account.club
    except ObjectDoesNotExist:  # No club associated with user,
        return render(request, template_name='actions/no_club_account.html')
    club_teams_id = list(club.teams.all().values_list('id', flat=True))
    if team_id not in club_teams_id:  # user is not allowed to see this team
        return render(request, template_name='actions/restricted_access.html')

    team = get_object_or_404(Team, id=team_id)

    # FILTER RESULTS
    actions = Action.objects.filter(Q(team=team_id) | Q(opp_team=team_id))
    actions_filter = ActionFilter(request.GET, queryset=actions, team_id=team_id)

    # PAGINATION
    paginator = Paginator(actions_filter.qs, 5)  # show 5 results per page
    default_page = 1
    page_number = request.GET.get('page', default_page)
    try:
        page_results = paginator.page(page_number)
    except PageNotAnInteger:
        page_results = paginator.page(default_page)
    except EmptyPage:
        page_results = paginator.page(paginator.num_pages)

    content = {'team': team, 'page_results': page_results, 'action_filter': actions_filter}
    return render(request, template_name='actions/team_actions.html',
                  context=content)


@login_required
def edit_action_view(request, action_id):

    # CHECK USER ALLOWANCE,
    # TODO authentication and permission system
    try:
        club = request.user.account.club
    except ObjectDoesNotExist:  # No club associated with user,
        return render(request, template_name='actions/no_club_account.html')
    club_teams_id = set(club.teams.all().values_list('id', flat=True))

    action = get_object_or_404(Action, id=action_id)
    # TODO check if club or team was deleted and team.id is None
    if action.team.id in club_teams_id:  # user team attacking
        my_team_attack = True
        my_team_id = action.team.id
    elif action.opp_team.id in club_teams_id:  # user team defending
        my_team_attack = False
        my_team_id = action.opp_team.id
    else:  # action not belongs to this club/user
        return render(request, template_name='actions/restricted_access.html')

    form = ActionForm(instance=action, team_id=my_team_id,
                      my_team_attack=my_team_attack, action_type_id=action.type.id)

    content = {'action': action, 'my_team_attack': my_team_attack, 'form': form}
    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action, team_id=my_team_id,
                          my_team_attack=my_team_attack, action_type_id=action.type.id)
        if form.is_valid():
            form.save()
        return redirect(request.path)  # to avoid page reload and re-submit data

    return render(request, template_name='actions/action_edit.html',
                  context=content)
