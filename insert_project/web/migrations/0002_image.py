# Generated by Django 5.1.4 on 2024-12-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=255, verbose_name='账户')),
                ('chinese_name', models.CharField(max_length=255, verbose_name='中文学名')),
            ],
            options={
                'verbose_name': '收藏',
                'verbose_name_plural': '收藏',
                'db_table': 'Image',
            },
        ),
    ]
