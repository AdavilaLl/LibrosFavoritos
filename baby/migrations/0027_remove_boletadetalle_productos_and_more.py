# Generated by Django 4.0.1 on 2022-03-23 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0026_alter_boletadetalle_boleta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boletadetalle',
            name='productos',
        ),
        migrations.AddField(
            model_name='boletadetalle',
            name='productos',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='boletaDetalle', to='baby.product'),
        ),
    ]
