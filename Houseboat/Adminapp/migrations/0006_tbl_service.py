# Generated by Django 4.1 on 2024-01-23 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0005_tbl_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_service',
            fields=[
                ('serviceid', models.AutoField(primary_key=True, serialize=False)),
                ('servicename', models.CharField(max_length=100)),
                ('serviceamount', models.BigIntegerField()),
            ],
        ),
    ]
