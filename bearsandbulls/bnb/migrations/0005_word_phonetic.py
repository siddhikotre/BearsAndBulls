# Generated by Django 4.1.5 on 2023-01-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bnb', '0004_gamelog_rough_alter_gamelog_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='phonetic',
            field=models.CharField(default='phonetic not available', max_length=200),
        ),
    ]
