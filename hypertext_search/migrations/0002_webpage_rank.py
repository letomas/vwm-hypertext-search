# Generated by Django 2.2 on 2019-05-10 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hypertext_search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='rank',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
