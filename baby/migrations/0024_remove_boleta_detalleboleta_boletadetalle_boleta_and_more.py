# Generated by Django 4.0.1 on 2022-03-22 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0023_rename_boletaitem_boletadetalle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boleta',
            name='detalleBoleta',
        ),
        migrations.AddField(
            model_name='boletadetalle',
            name='boleta',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='boletas', to='baby.boleta'),
        ),
        migrations.RemoveField(
            model_name='boletadetalle',
            name='productos',
        ),
        migrations.AddField(
            model_name='boletadetalle',
            name='productos',
            field=models.ManyToManyField(related_name='productos', to='baby.Product'),
        ),
    ]
