# Generated by Django 4.0.1 on 2022-03-20 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0014_buycart_estado_buycart_precioenvio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buycart',
            name='productos',
            field=models.ManyToManyField(related_name='productos', to='baby.Product'),
        ),
    ]
