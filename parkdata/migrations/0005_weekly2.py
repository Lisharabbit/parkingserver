# Generated by Django 2.0.1 on 2018-05-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkdata', '0004_weekly1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekly2',
            fields=[
                ('id', models.IntegerField(db_column='Id', primary_key=True, serialize=False)),
                ('blockid', models.IntegerField(db_column='BlockId')),
                ('period', models.IntegerField(db_column='Period')),
                ('weekday', models.IntegerField(db_column='Weekday')),
                ('prob', models.FloatField(db_column='Prob')),
                ('predicted', models.FloatField(db_column='Predicted')),
            ],
            options={
                'db_table': 'Weekly2',
                'managed': False,
            },
        ),
    ]