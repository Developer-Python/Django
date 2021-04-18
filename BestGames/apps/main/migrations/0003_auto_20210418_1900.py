# Generated by Django 3.2 on 2021-04-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210417_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background', models.ImageField(upload_to='themes/', verbose_name='Фон сайта')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='author_image',
            field=models.ImageField(blank=True, upload_to='users/', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(upload_to='users/', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_1',
            field=models.ImageField(upload_to='games/2021-04-18', verbose_name='1) Изображение из игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_2',
            field=models.ImageField(upload_to='games/2021-04-18', verbose_name='2) Изображение из игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_3',
            field=models.ImageField(upload_to='games/2021-04-18', verbose_name='3) Изображение из игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_4',
            field=models.ImageField(upload_to='games/2021-04-18', verbose_name='4) Изображение из игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image_wrapper',
            field=models.ImageField(upload_to='games/', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Дата публикаций игры на сайте'),
        ),
    ]