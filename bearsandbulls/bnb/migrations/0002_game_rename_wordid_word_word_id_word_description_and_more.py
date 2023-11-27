# Generated by Django 4.1.5 on 2023-01-22 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bnb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField()),
                ('game_id', models.IntegerField()),
                ('game_date', models.DateField(auto_now_add=True)),
                ('opponent_id', models.IntegerField(default=0)),
                ('is_active', models.IntegerField(default=0)),
                ('player_mode', models.CharField(max_length=20)),
                ('word_length', models.IntegerField()),
                ('difficulty', models.CharField(max_length=20)),
                ('word', models.CharField(max_length=20)),
                ('p1_score', models.IntegerField(default=0)),
                ('p2_score', models.IntegerField(default=0)),
                ('winner', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='word',
            old_name='wordid',
            new_name='word_id',
        ),
        migrations.AddField(
            model_name='word',
            name='description',
            field=models.CharField(default='Description not available', max_length=200),
        ),
        migrations.AddField(
            model_name='word',
            name='difficulty',
            field=models.CharField(default='easy', max_length=20),
        ),
        migrations.AddField(
            model_name='word',
            name='length',
            field=models.IntegerField(default=4),
        ),
    ]
