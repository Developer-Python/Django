# Generated by Django 3.1 on 2020-12-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201211_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата публикаций игры на сайте'),
        ),
        migrations.AlterField(
            model_name='game',
            name='data',
            field=models.IntegerField(default=0, verbose_name='Дата выхода игры'),
        ),
    ]