# Generated by Django 3.2.15 on 2022-09-26 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20220926_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='foods.Tag', verbose_name='Теги'),
        ),
    ]
