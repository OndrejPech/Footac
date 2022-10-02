from django.forms import ModelForm
from .models import Action, Player
from django import forms
from .db_data import ACTIONS_IDS as ID

# ids,of actions_type where passive_player can not be from attacking team:
no_passive_player_ids = {ID['shot'], ID['foul'], ID['goal'], ID['penalty kick'],
                         ID['yellow card'], ID['red card'], ID['lob']}
# ids,of actions_type where passive_player has to be from attacking team:
attacking_team_only_ids = {ID['substitution']}
# in other action_type passive player can be from attacking or defending team


class ActionForm(ModelForm):
    def __init__(self, *args, team_id, my_team_attack, action_type_id,
                 **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)  # populates the post

        self.fields['active_player'].label = 'Aktivní hráč'
        self.fields['passive_player'].label = 'Pasivní hráč'
        if my_team_attack:
            self.fields['active_player'].queryset = Player.objects.filter(
                teams=team_id)
            if action_type_id in no_passive_player_ids:
                self.fields[
                    'passive_player'].widget = forms.HiddenInput()  # Hide field
            else:
                self.fields['passive_player'].queryset = Player.objects.filter(
                    teams=team_id)

        else:
            self.fields[
                'active_player'].widget = forms.HiddenInput()  # Hide field
            if action_type_id in attacking_team_only_ids:
                self.fields['passive_player'].widget = forms.HiddenInput()
            else:
                self.fields['passive_player'].queryset = Player.objects.filter(
                    teams=team_id)

    class Meta:
        model = Action
        fields = ['active_player', 'passive_player']
