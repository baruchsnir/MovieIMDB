# Generated by Django 3.0.4 on 2020-03-22 16:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('actorid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('photo', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movieid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('year', models.CharField(max_length=4)),
                ('length', models.CharField(max_length=10)),
                ('genres', models.CharField(max_length=100)),
                ('rate', models.IntegerField(default=0)),
                ('poster', models.URLField(default='')),
                ('plot', models.CharField(max_length=500)),
                ('trailer', models.URLField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Seen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('movieid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('movieid', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Popularity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0)),
                ('movieid', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='movie.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Expect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('movieid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actorid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.Actor')),
                ('movieid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie')),
            ],
        ),
    ]
