# Generated by Django 4.0.6 on 2022-08-23 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0013_alter_club_address_alter_club_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='link_1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='link_2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='link_3',
            field=models.URLField(blank=True, null=True),
        ),
    ]
