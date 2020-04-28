# Generated by Django 2.2.10 on 2020-04-28 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('url', models.URLField(unique=True, verbose_name='Ссылка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('language', models.CharField(choices=[('RU', 'Русский'), ('EN', 'English')], max_length=2, verbose_name='Язык')),
                ('approved', models.BooleanField(default=False, verbose_name='Одобрено модератором')),
                ('group', models.ManyToManyField(blank=True, related_name='tags_posts', to='posts.Group', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
            },
        ),
    ]
