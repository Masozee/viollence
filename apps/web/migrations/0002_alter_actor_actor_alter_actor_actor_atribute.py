# Generated by Django 5.0.6 on 2024-07-25 01:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='actor',
            field=models.ForeignKey(limit_choices_to={'category': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='incident_actor', to='web.options'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='actor_atribute',
            field=models.ForeignKey(limit_choices_to={'category': 4}, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_actor', to='web.options'),
        ),
    ]
