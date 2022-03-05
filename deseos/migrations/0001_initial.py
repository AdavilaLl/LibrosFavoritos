# Generated by Django 4.0.3 on 2022-03-05 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100, verbose_name='contrasenia')),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users_who_like', models.ManyToManyField(related_name='liked_wishes', to='deseos.user')),
                ('wished_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes_uploaded', to='deseos.user')),
            ],
        ),
    ]
