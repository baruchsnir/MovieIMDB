# Generated by Django 3.0.4 on 2020-03-22 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='movieid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie'),
        ),
    ]
