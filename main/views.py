from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserProfile, UserSettings


def calculate_bmr(weight, height, age, gender, formula, energy_unit, percentage_of_fat=None):
    bmr = None

    if formula == 'mifflin_st_jeor':
        bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'male' else -161)

    elif formula == 'harris_benedict':
        if gender == 'male':
            bmr = 66.5 + 13.75 * weight + 5.003 * height - 6.755 * age
        else:
            bmr = 655.1 + 9.563 * weight + 1.850 * height - 4.676 * age

    elif formula == 'katch_mcardle':
        if percentage_of_fat is None:
            raise ValueError("percentage_of_fat is required for Katch-McArdle formula")
        lean_body_mass = weight * (1 - percentage_of_fat / 100)
        bmr = 370 + (21.6 * lean_body_mass)

    if bmr is not None:
        if energy_unit == 'kj':
            return round(bmr * 4.184)
        else:
            return round(bmr)

    return None


def calculate_bmi(weight, height):
    height_m = height / 100  # см → метры
    return round(weight / (height_m ** 2), 2)


activity_map = {
    'low': 0,
    'moderate': 250,
    'high': 500,
    'very_high': 500,
    'hyperactive': 750
}


def calculate_water_intake(weight_kg, activity_level):
    activity_additional_ml = activity_map.get(activity_level, 0)
    base_intake = weight_kg * 31
    total_intake = base_intake + activity_additional_ml

    rounded_intake = round(total_intake / 250) * 250
    return int(rounded_intake)


DIET_PRESETS = {
    'standard': {'carbs': 50, 'protein': 20, 'fat': 30},
    'balanced': {'carbs': 50, 'protein': 25, 'fat': 25},
    'lowfat': {'carbs': 60, 'protein': 25, 'fat': 15},
    'highprotein': {'carbs': 25, 'protein': 40, 'fat': 35},
    'keto': {'carbs': 5, 'protein': 30, 'fat': 65},
}


def convert_water_ml(value_ml, unit):
    if unit == 'oz':
        return round(value_ml / 29.5735)
    elif unit == 'cups':
        return int(value_ml / 250)
    return value_ml


def home_page(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {
            'error': "You must be logged in to view this data."
        })

    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        settings, created = UserSettings.objects.get_or_create(user=request.user)

        weight = profile.weight_kg
        height = profile.height_cm
        age = profile.age
        gender = profile.gender
        formula = settings.formula
        activity_level = profile.activity_level
        percentage_of_fat = profile.fat_percentage

        energy_unit = settings.energy_unit
        bmr = calculate_bmr(weight, height, age, gender, formula, energy_unit, percentage_of_fat)
        bmi = calculate_bmi(weight, height)

        water = calculate_water_intake(weight, activity_level)
        water_unit = settings.water_unit
        converted_water = convert_water_ml(water, water_unit)

        diet_type = request.POST.get('diet_type', 'standard')
        macro_ratios = DIET_PRESETS.get(diet_type, DIET_PRESETS['standard'])

        carbs_ratio = macro_ratios['carbs'] / 100
        protein_ratio = macro_ratios['protein'] / 100
        fat_ratio = macro_ratios['fat'] / 100

        carbs_energy = bmr * carbs_ratio
        protein_energy = bmr * protein_ratio
        fat_energy = bmr * fat_ratio

        carbs_g = round(carbs_energy / (4 * 4.184) if energy_unit == 'kj' else carbs_energy / 4)
        protein_g = round(protein_energy / (4 * 4.184) if energy_unit == 'kj' else protein_energy / 4)
        fat_g = round(fat_energy / (9 * 4.184) if energy_unit == 'kj' else fat_energy / 9)

        return render(request, 'main/home.html', {
            'bmr': bmr,
            'bmi': bmi,
            'water': converted_water,
            'water_unit_label': water_unit,
            'energy_unit_label': energy_unit,
            'diet_type': diet_type,
            'carbs_g': carbs_g,
            'protein_g': protein_g,
            'fat_g': fat_g,
            'carbs_energy': round(carbs_energy),
            'protein_energy': round(protein_energy),
            'fat_energy': round(fat_energy),
        })

    except UserProfile.DoesNotExist:
        return render(request, 'main/home.html', {
            'error': "User profile not found."
        })
    except UserSettings.DoesNotExist:
        return render(request, 'main/home.html', {
            'error': "User settings not found."
        })
