# Generated by Django 4.2.4 on 2023-10-27 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_customuser_email_verificado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email_verificado',
        ),
    ]
