# Generated by Django 4.1.13 on 2024-04-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_user_approver_remove_user_is_approver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ci',
            field=models.IntegerField(default=0),
        ),
    ]
