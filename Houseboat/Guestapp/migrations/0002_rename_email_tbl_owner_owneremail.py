# Generated by Django 4.1 on 2024-01-25 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guestapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbl_owner',
            old_name='email',
            new_name='owneremail',
        ),
    ]
