# Generated by Django 2.2 on 2020-10-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredents',
            field=models.TextField(),
        ),
    ]
