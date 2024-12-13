# Generated by Django 4.1 on 2024-01-23 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0004_tbl_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_package',
            fields=[
                ('packageid', models.AutoField(primary_key=True, serialize=False)),
                ('packagename', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('amount', models.BigIntegerField()),
                ('days', models.CharField(max_length=30)),
            ],
        ),
    ]