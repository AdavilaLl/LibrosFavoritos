# Generated by Django 4.0.1 on 2022-03-18 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0008_alter_product_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cantVendidos',
            field=models.IntegerField(default=0),
        ),
    ]
