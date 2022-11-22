from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from actions.models import Club, Team, Game, Action
from actions.filters import ActionFilter
from actions.forms import ActionForm
from actions.db_data import ACTIONS_IDS


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
        return render(request, template_name='actions/restricted_access.html')
    club_teams_id = list(club.teams.all().values_list('id', flat=True))
    if team_id not in club_teams_id:  # user is not allowed to see this team
        return render(request, template_name='actions/restricted_access.html')

    team = get_object_or_404(Team, id=team_id)

    # FILTER RESULTS
    actions = Action.objects.filter(Q(team=team_id) | Q(opp_team=team_id))
    actions_filter = ActionFilter(request.GET, queryset=actions, team_id=team_id)

    # PAGINATION
    paginator = Paginator(actions_filter.qs, 25)  # show 25 results per page
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
    try:
        club = request.user.account.club
    except ObjectDoesNotExist:  # No club associated with user,
        return render(request, template_name='actions/restricted_access.html')
    club_teams_id = set(club.teams.all().values_list('id', flat=True))

    action = get_object_or_404(Action, id=action_id)
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

    content = {'action': action, 'my_team_attack': my_team_attack, 'form': form, 'team_id': my_team_id}
    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action, team_id=my_team_id,
                          my_team_attack=my_team_attack, action_type_id=action.type.id)
        if form.is_valid():
            form.save()
        return redirect(request.path)  # to avoid page reload and re-submit data

    return render(request, template_name='actions/action_edit.html',
                  context=content)


@login_required()
def game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    home_team_id = game.home_team_id
    away_team_id = game.away_team_id

    home_team_act = Action.objects.filter(team_id=home_team_id, game=game)
    away_team_act = Action.objects.filter(team_id=away_team_id, game=game)

    data = {}

    def fill_data(action_type, id):
        """
        find out count from DB for home team and away team, save it to data dict
        """
        home_name_string = f'home_{action_type.replace(" ", "_")}'
        away_name_string = f'away_{action_type.replace(" ", "_")}'

        data[home_name_string] = home_team_act.filter(type_id=id).count()
        data[away_name_string] = away_team_act.filter(type_id=id).count()

    # fetch all counts from DB, is executing QUERY 24x to get different counts
    # need to optimize in the future
    for action_type, action_id in ACTIONS_IDS.items():
        fill_data(action_type, action_id)

    content = {'game': game, 'data': data}
    return render(request, template_name='actions/game_detail.html',
                  context=content)
