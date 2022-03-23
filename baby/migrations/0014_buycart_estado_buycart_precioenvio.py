# Generated by Django 4.0.1 on 2022-03-20 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0013_buycart'),
    ]

    operations = [
        migrations.AddField(
            model_name='buycart',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buycart',
            name='precioEnvio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
