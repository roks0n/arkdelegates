# Generated by Django 2.0.5 on 2018-05-26 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_history_rank_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='delegate_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='app.Delegate'),
        ),
    ]
