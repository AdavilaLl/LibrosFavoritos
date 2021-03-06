# Generated by Django 4.0.1 on 2022-03-22 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baby', '0015_alter_buycart_productos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buycart',
            name='precioEnvio',
        ),
        migrations.RemoveField(
            model_name='buycart',
            name='productos',
        ),
        migrations.AddField(
            model_name='buycart',
            name='productos',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='baby.product'),
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('totalDesc', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('totalOpGravada', models.DecimalField(decimal_places=2, max_digits=6)),
                ('totalIGV', models.DecimalField(decimal_places=2, max_digits=6)),
                ('precioEnvio', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pagado', models.BooleanField(default=False)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carritos', to='baby.buycart')),
            ],
        ),
    ]
