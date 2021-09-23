# Generated by Django 3.2.7 on 2021-09-21 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='urltoken',
            field=models.UUIDField(),
        ),
    ]