# Generated by Django 4.0.3 on 2022-05-29 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='Priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.prioritys'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='Severity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.severitys'),
        ),
    ]
