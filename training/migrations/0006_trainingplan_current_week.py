# Generated by Django 5.0.6 on 2025-07-12 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_alter_fitnesstestresult_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingplan',
            name='current_week',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
