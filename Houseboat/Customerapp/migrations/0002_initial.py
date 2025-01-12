# Generated by Django 4.1 on 2024-02-27 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Ownerapp', '0001_initial'),
        ('Customerapp', '0001_initial'),
        ('Guestapp', '0005_tbl_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_request',
            name='boatid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ownerapp.tbl_boat'),
        ),
        migrations.AddField(
            model_name='tbl_request',
            name='customerid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Guestapp.tbl_customer'),
        ),
    ]
