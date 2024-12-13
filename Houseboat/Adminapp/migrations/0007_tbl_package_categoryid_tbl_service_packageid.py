# Generated by Django 4.1 on 2024-02-05 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0006_tbl_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_package',
            name='categoryid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_category'),
        ),
        migrations.AddField(
            model_name='tbl_service',
            name='packageid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Adminapp.tbl_package'),
        ),
    ]