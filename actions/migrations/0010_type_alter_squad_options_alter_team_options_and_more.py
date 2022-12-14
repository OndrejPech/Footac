# Generated by Django 4.0.6 on 2022-08-10 10:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0009_alter_team_squad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('name_cz', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterModelOptions(
            name='squad',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='game',
            name='away_score',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_score',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.CreateModel(
            name='Subtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('name_cz', models.CharField(max_length=64)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtypes', to='actions.type')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('start_x', models.IntegerField(blank=True, null=True)),
                ('start_y', models.IntegerField(blank=True, null=True)),
                ('end_x', models.IntegerField(blank=True, null=True)),
                ('end_y', models.IntegerField(blank=True, null=True)),
                ('active_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_player_actions', to='actions.player')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_actions', to='actions.game')),
                ('opp_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opp_team_actions', to='actions.team')),
                ('passive_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passive_player_actions', to='actions.player')),
                ('subtype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtype_actions', to='actions.subtype')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_actions', to='actions.team')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_actions', to='actions.type')),
            ],
            options={
                'ordering': ['-game', 'game_time'],
            },
        ),
    ]
