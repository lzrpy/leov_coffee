# Generated by Django 4.2.4 on 2023-12-05 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0061_alter_pedido_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupons',
            name='usuarios',
            field=models.TextField(blank=True, null=True),
        ),
    ]
