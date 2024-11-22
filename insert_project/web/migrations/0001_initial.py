# Generated by Django 5.1.3 on 2024-11-22 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kingdom', models.CharField(blank=True, max_length=255, null=True, verbose_name='界')),
                ('phylum', models.CharField(blank=True, max_length=255, null=True, verbose_name='门')),
                ('class_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='纲')),
                ('subclass_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='亚纲')),
                ('order', models.CharField(blank=True, max_length=255, null=True, verbose_name='目')),
                ('family', models.CharField(blank=True, max_length=255, null=True, verbose_name='科')),
                ('genus', models.CharField(blank=True, max_length=255, null=True, verbose_name='属')),
                ('species', models.CharField(blank=True, max_length=255, null=True, verbose_name='种')),
                ('subspecies', models.CharField(blank=True, max_length=255, null=True, verbose_name='亚种')),
            ],
            options={
                'verbose_name': '物种信息',
                'verbose_name_plural': '物种信息',
                'db_table': 'taxonomy',
            },
        ),
        migrations.CreateModel(
            name='Insect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='俗名')),
                ('chinese_name', models.CharField(max_length=255, verbose_name='中文学名')),
                ('latin_name', models.CharField(max_length=255, unique=True, verbose_name='拉丁文')),
                ('aliases', models.TextField(blank=True, null=True, verbose_name='别名')),
                ('appearance', models.TextField(blank=True, null=True, verbose_name='外貌形态')),
                ('habits', models.TextField(blank=True, null=True, verbose_name='习性')),
                ('distribution', models.TextField(blank=True, null=True, verbose_name='分布')),
                ('relatives', models.TextField(blank=True, null=True, verbose_name='近亲')),
                ('taxonomy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.taxonomy', verbose_name='物种信息')),
            ],
            options={
                'verbose_name': '昆虫',
                'verbose_name_plural': '昆虫',
                'db_table': 'insect',
            },
        ),
    ]
