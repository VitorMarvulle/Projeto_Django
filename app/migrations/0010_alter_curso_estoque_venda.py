# Generated by Django 5.1.2 on 2024-12-05 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_curso_estoque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='estoque',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_venda', models.DateTimeField(auto_now_add=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='app.curso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='app.usuario')),
            ],
        ),
    ]