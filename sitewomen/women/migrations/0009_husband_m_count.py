# Generated by Django 5.0 on 2024-01-16 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0008_husband_women_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='husband',
            name='m_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
