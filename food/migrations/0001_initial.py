# Generated by Django 5.0.6 on 2025-07-10 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('serving_sizes', models.FloatField(blank=True, default=100)),
                ('calories', models.FloatField()),
                ('fat', models.FloatField()),
                ('saturated', models.FloatField(blank=True, null=True)),
                ('polyunsaturated', models.FloatField(blank=True, null=True)),
                ('monounsaturated', models.FloatField(blank=True, null=True)),
                ('trans', models.FloatField(blank=True, null=True)),
                ('cholesterol', models.FloatField(blank=True, null=True)),
                ('salt', models.FloatField(blank=True, null=True)),
                ('sodium', models.FloatField(blank=True, null=True)),
                ('potassium', models.FloatField(blank=True, null=True)),
                ('carbohydrate', models.FloatField()),
                ('dietary_fiber', models.FloatField(blank=True, null=True)),
                ('sugars', models.FloatField(blank=True, null=True)),
                ('protein', models.FloatField()),
                ('vitamin_a', models.FloatField(blank=True, null=True)),
                ('vitamin_c', models.FloatField(blank=True, null=True)),
                ('calcium', models.FloatField(blank=True, null=True)),
                ('iron', models.FloatField(blank=True, null=True)),
                ('magnesium', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='MealEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(null=True)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='food.meal')),
            ],
        ),
        migrations.CreateModel(
            name='MealItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('amount', models.FloatField(default=1.0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('meal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food.mealentry')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('by_serving_of', models.FloatField(verbose_name='By serving of')),
                ('measurement_unit', models.CharField(choices=[('servings', 'servings'), ('g', 'grams'), ('ml', 'milliliters'), ('oz', 'ounces'), ('fl_oz', 'fluid ounces')], default='servings', max_length=10, verbose_name='Measurement unit')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('directions', models.TextField(blank=True, null=True, verbose_name='Directions')),
                ('ingredients', models.ManyToManyField(related_name='recipes', to='food.food', verbose_name='Ingredients')),
            ],
        ),
    ]
