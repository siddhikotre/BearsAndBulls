# Generated by Django 4.1.5 on 2023-01-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordid', models.IntegerField()),
                ('word', models.CharField(max_length=50)),
            ],
        ),
    ]
