# Generated by Django 4.1 on 2024-02-06 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0007_tbl_package_categoryid_tbl_service_packageid'),
        ('Guestapp', '0004_remove_tbl_owner_districtid'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_customer',
            fields=[
                ('customerid', models.AutoField(primary_key=True, serialize=False)),
                ('customername', models.CharField(max_length=100)),
                ('housename', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
                ('emailid', models.EmailField(max_length=100)),
                ('phoneno', models.BigIntegerField()),
                ('regdate', models.DateField(auto_now_add=True)),
                ('locationid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_location')),
                ('loginid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guestapp.tbl_login')),
            ],
        ),
    ]
