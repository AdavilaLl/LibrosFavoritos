# Generated by Django 4.0.3 on 2022-03-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deseos', '0002_remove_wish_users_who_like_wish_users_who_granted'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='users_who_liked',
            field=models.ManyToManyField(related_name='liked_wishes', to='deseos.user'),
        ),
    ]