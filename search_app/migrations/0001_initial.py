# Generated by Django 3.2.5 on 2022-11-14 17:15

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import search_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MovieDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.TextField(db_index=True)),
                ('director', models.TextField(db_index=True)),
                ('movie_popularity', models.FloatField(default=0.0, validators=[search_app.models.validate_interval_for_popularity])),
                ('imdb_rating', models.FloatField(default=0.0, validators=[search_app.models.validate_interval_for_ratings])),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.TextField(unique=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='moviegenre',
            index=models.Index(fields=['genre_name'], name='search_app__genre_n_9f4c68_idx'),
        ),
        migrations.AddField(
            model_name='moviedetails',
            name='genres',
            field=models.ManyToManyField(related_name='genre', to='search_app.MovieGenre'),
        ),
        migrations.AddField(
            model_name='users',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='moviedetails',
            index=models.Index(fields=['movie_name'], name='search_app__movie_n_1e7374_idx'),
        ),
        migrations.AddIndex(
            model_name='moviedetails',
            index=models.Index(fields=['director'], name='search_app__directo_d487b9_idx'),
        ),
        migrations.AddConstraint(
            model_name='moviedetails',
            constraint=models.UniqueConstraint(fields=('movie_name', 'director'), name='unique_migration_host_combination'),
        ),
    ]
