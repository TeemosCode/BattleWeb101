# Generated by Django 2.1.2 on 2018-12-13 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttackedHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid_x', models.IntegerField()),
                ('grid_y', models.IntegerField()),
            ],
            options={
                'ordering': ['grid_x', 'grid_y'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.AutoField(primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=15)),
                ('player_bullets', models.IntegerField(default=3)),
                ('player_hit_points', models.IntegerField(default=20)),
                ('player_suncker_points', models.IntegerField(default=0)),
                ('player_total_shots', models.IntegerField(default=0)),
                ('player_total_hits', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['player_id'],
            },
        ),
        migrations.AddField(
            model_name='grid',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grid', to='BattleWeb101.Player'),
        ),
        migrations.AddField(
            model_name='attackedhistory',
            name='attacker_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attacker', to='BattleWeb101.Player'),
        ),
        migrations.AddField(
            model_name='attackedhistory',
            name='victim_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='victim', to='BattleWeb101.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='grid',
            unique_together={('player', 'grid_x', 'grid_y')},
        ),
        migrations.AlterUniqueTogether(
            name='attackedhistory',
            unique_together={('attacker_id', 'victim_id')},
        ),
    ]
