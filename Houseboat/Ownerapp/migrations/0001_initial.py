# Generated by Django 4.1 on 2024-02-27 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Adminapp', '0007_tbl_package_categoryid_tbl_service_packageid'),
        ('Guestapp', '0005_tbl_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_boat',
            fields=[
                ('boatid', models.AutoField(primary_key=True, serialize=False)),
                ('boatname', models.CharField(max_length=30, null=True)),
                ('boatamount', models.BigIntegerField(default=None)),
                ('regdate', models.DateField(auto_now_add=True)),
                ('boatimage', models.ImageField(upload_to='')),
                ('categoryid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_category')),
                ('loginid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Guestapp.tbl_login')),
                ('packageid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_package')),
                ('serviceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_service')),
            ],
        ),
    ]
