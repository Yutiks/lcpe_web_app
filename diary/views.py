import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserProfile, UserSettings
from django.views.decorators.http import require_POST
from food.models import Food, Meal, MealEntry, Recipe
from .models import DiarySettings, DailyLog
from main.views import calculate_water_intake, calculate_bmr, DIET_PRESETS
from datetime import datetime, timedelta
from content.models import UserContent
from training.models.exercise_session import Exercise


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("Unsupported date format")


def sync_meals_with_daily_logs(user):
    user_meals = Meal.objects.filter(user=user).order_by('id')
    for log in DailyLog.objects.filter(user=user):
        current_entries = log.meals.select_related('meal').all()
        current_meals = set(entry.meal for entry in current_entries)

        # Meals to add
        for meal in user_meals:
            if meal not in current_meals:
                entry = MealEntry.objects.create(meal=meal, time=None)
                log.meals.add(entry)

        # Meals to remove
        for entry in current_entries:
            if entry.meal not in user_meals:
                log.meals.remove(entry)
                entry.delete()


def create_default_meals(user):
    meals = Meal.objects.filter(user=user).order_by('id')
    if not meals.exists():
        default_meals = ['Breakfast', 'Lunch', 'Dinner']
        for meal_name in default_meals:
            Meal.objects.create(name=meal_name, user=user)


def calculate_macro_goals(bmr, macro_ratios, energy_unit):
    if energy_unit == 'kj':
        carb_divisor = protein_divisor = 4 * 4.184
        fat_divisor = 9 * 4.184
    else:
        carb_divisor = protein_divisor = 4
        fat_divisor = 9

    carbs_goal_g = round((bmr * macro_ratios['carbs'] / 100) / carb_divisor)
    protein_goal_g = round((bmr * macro_ratios['protein'] / 100) / protein_divisor)
    fat_goal_g = round((bmr * macro_ratios['fat'] / 100) / fat_divisor)

    return carbs_goal_g, protein_goal_g, fat_goal_g


@login_required
def diary(request):
    date_str = request.GET.get('date')

    try:
        if date_str:
            current_date = parse_date(date_str)
        else:
            current_date = datetime.today().date()
    except ValueError:
        current_date = datetime.today().date()

    create_default_meals(request.user)
    sync_meals_with_daily_logs(request.user)

    daily_log, created = DailyLog.objects.get_or_create(user=request.user, date=current_date)
    if created:
        for meal in Meal.objects.filter(user=request.user):
            entry = MealEntry.objects.create(meal=meal, time=None)
            daily_log.meals.add(entry)

    meals = daily_log.meals.select_related('meal').prefetch_related('items__content_type').all().order_by('id')
    for entry in meals:
        food_items = []
        recipe_items = []
        for item in entry.items.all():
            obj = item.food_or_recipe
            if isinstance(obj, Food):
                food_items.append(item)
            elif isinstance(obj, Recipe):
                recipe_items.append(item)
        entry.food_items = food_items
        entry.recipe_items = recipe_items
    exercises = daily_log.exercises.all()
    water = daily_log.water_intake_ml

    diary_settings, created = DiarySettings.objects.get_or_create(user=request.user)

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    weight = profile.weight_kg
    height = profile.height_cm
    age = profile.age
    gender = profile.gender
    activity_level = profile.activity_level
    percentage_of_fat = profile.fat_percentage

    formula = settings.formula

    water_goal = calculate_water_intake(weight, activity_level)

    energy_unit = settings.energy_unit
    bmr = calculate_bmr(weight, height, age, gender, formula, energy_unit, percentage_of_fat)

    macro_ratios = DIET_PRESETS.get(settings.diet_type, DIET_PRESETS['standard'])

    carbs_goal_g, protein_goal_g, fat_goal_g = calculate_macro_goals(bmr, macro_ratios, energy_unit)

    total_carbs = 0
    total_protein = 0
    total_fat = 0
    total_energy = 0
    exercise_energy = 0

    for entry in meals:
        for item in entry.items.all():
            food = item.food_or_recipe
            if not isinstance(food, Food):
                continue

            weight_ratio = item.amount
            total_carbs += (food.carbohydrate or 0) * weight_ratio
            total_protein += (food.protein or 0) * weight_ratio
            total_fat += (food.fat or 0) * weight_ratio
            total_energy += (food.calories or 0) * weight_ratio

    for exercise in exercises:
        exercise_energy += exercise.calories_burned or 0

    total_carbs = round(total_carbs)
    total_protein = round(total_protein)
    total_fat = round(total_fat)
    total_energy = round(total_energy - exercise_energy)

    if energy_unit == 'kj':
        total_energy_kj = round(total_energy * 4.184)
        total_energy = total_energy_kj

    water_unit = settings.water_unit
    water_display, water_goal_display, label = unit_converter(water_unit, water, water_goal)

    def percent(value, goal):
        return int((value / goal) * 100) if value > 0 else 0

    context = {
        'current_date': current_date,
        'prev_date': (current_date - timedelta(days=1)).isoformat(),
        'next_date': (current_date + timedelta(days=1)).isoformat(),
        'bmr': bmr,
        'carbs': total_carbs,
        'protein': total_protein,
        'fat': total_fat,
        'energy': total_energy,
        'carbs_goal': carbs_goal_g,
        'protein_goal': protein_goal_g,
        'fat_goal': fat_goal_g,
        'water_unit': water_unit,
        'label': label,
        'energy_unit_label': energy_unit,
        'water_display': water_display,
        'water_goal_display': water_goal_display,
        'energy_percentage': percent(total_energy, bmr),
        'carbs_percentage': percent(total_carbs, carbs_goal_g),
        'protein_percentage': percent(total_protein, protein_goal_g),
        'fat_percentage': percent(total_fat, fat_goal_g),
        'water_percentage': percent(water, water_goal),
        'meals': meals,
        'exercises': exercises,
        'show_water': diary_settings.show_water_tracker,
        'show_exercise': diary_settings.show_exercise_tracker,
        'show_meal_time': diary_settings.show_meals_time,
    }

    return render(request, 'diary/diary.html', context)


@login_required
def settings_diary(request):
    diary_settings, _ = DiarySettings.objects.get_or_create(user=request.user)
    return render(request, 'diary/settings_diary.html', {'diary_settings': diary_settings})


@csrf_exempt
@login_required
def update_diary_setting(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        diary_settings, _ = DiarySettings.objects.get_or_create(user=request.user)
        if field in ['show_water_tracker', 'show_exercise_tracker', 'show_meals_time']:
            setattr(diary_settings, field, value)
            diary_settings.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def update_water(request, direction):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({'error': 'Invalid date'}, status=400)

    try:
        log_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    profile = UserProfile.objects.get(user=request.user)
    water_goal = calculate_water_intake(profile.weight_kg, profile.activity_level)
    user_settings = UserSettings.objects.get(user=request.user)
    daily_log, _ = DailyLog.objects.get_or_create(user=request.user, date=log_date)
    water_unit = user_settings.water_unit

    if water_unit == "oz":
        step = 236  # 8 oz
    else:
        step = 250  # 250 ml

    if direction == 'plus':
        daily_log.water_intake_ml = min(daily_log.water_intake_ml + step, water_goal)
    elif direction == 'minus':
        daily_log.water_intake_ml = max(daily_log.water_intake_ml - step, 0)
    else:
        return JsonResponse({'error': 'Invalid direction'}, status=400)

    daily_log.save()

    percentage = round((daily_log.water_intake_ml / water_goal) * 100)
    ml = daily_log.water_intake_ml
    water_intake, water_goal_converted, _ = unit_converter(water_unit, ml, water_goal)

    return JsonResponse({
        'water': water_intake,
        'goal': water_goal_converted,
        'percentage': percentage,
        'water_unit': water_unit,
    })


def unit_converter(water_unit, ml, goal_ml):
    if water_unit == 'oz':
        water_intake = round(ml / 29.5735)
        water_goal = round(goal_ml / 29.5735)
        label = "8 oz"
    elif water_unit == 'cups':
        water_intake = round(ml / 250)
        water_goal = round(goal_ml / 250)
        label = "1 cup"
    else:
        water_intake = ml
        water_goal = goal_ml
        label = "250 ml"
    return water_intake, water_goal, label


@login_required
def add_exercise_to_diary(request):
    user_content, created = UserContent.objects.get_or_create(user=request.user)
    tab = request.GET.get('tab', 'my_exercises')
    query = request.GET.get('search', '').strip()
    date = request.GET.get('date')

    if tab == 'my_exercises':
        if query:
            results = user_content.my_exercises.filter(name__icontains=query)
        else:
            results = user_content.my_exercises.all()

    elif tab == 'library':
        if query:
            results = Exercise.objects.filter(user__isnull=True, name__icontains=query)
        else:
            results = Exercise.objects.filter(user__isnull=True)

    else:
        results = []

    return render(request, 'diary/add_exercise_to_diary.html', {
        'tab': tab,
        'results': results,
        'query': query,
        'date': date
    })


@login_required
@require_POST
def add_exercise_to_log(request):
    exercise_id = request.POST.get('exercise_id')
    date = request.POST.get('date')
    parsed_date = datetime.strptime(date, '%B %d, %Y')
    date = parsed_date.strftime('%Y-%m-%d')
    if not exercise_id:
        return redirect('diary')

    exercise = get_object_or_404(Exercise, id=exercise_id)

    daily_log = DailyLog.objects.get(user=request.user, date=date)

    if exercise not in daily_log.exercises.all():
        daily_log.exercises.add(exercise)

    return redirect(f'/diary/?date={date}')


@require_POST
def remove_exercise(request, exercise_id):
    date = request.POST.get('date')
    parsed_date = datetime.strptime(date, '%B %d, %Y')
    date = parsed_date.strftime('%Y-%m-%d')
    daily_log = get_object_or_404(DailyLog, user=request.user, date=date)
    exercise = get_object_or_404(Exercise, id=exercise_id)

    daily_log.exercises.remove(exercise)

    return redirect(f'/diary/?date={date}')
