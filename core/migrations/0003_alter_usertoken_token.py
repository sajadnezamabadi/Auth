# Generated by Django 5.1.4 on 2024-12-14 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_usertoken_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(max_length=500),
        ),
    ]