# Generated by Django 3.1 on 2020-12-19 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_headers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='headers',
            new_name='header',
        ),
    ]