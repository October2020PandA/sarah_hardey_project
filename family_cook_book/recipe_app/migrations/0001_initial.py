# Generated by Django 2.2 on 2020-10-05 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('ingredents', models.CharField(max_length=225)),
                ('instructions', models.TextField()),
                ('image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ManyToManyField(related_name='liked_recipes', to='recipe_app.User')),
                ('recipe_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chef', to='recipe_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='recipe_app.User')),
            ],
        ),
    ]
