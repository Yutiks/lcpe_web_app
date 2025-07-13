from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import UserContent
from .forms import FoodForm, RecipeForm
from training.models.exercise_session import Exercise
from food.models import Food, Recipe
from accounts.models import UserSettings


@login_required
def my_exercises(request):
    try:
        user_content = UserContent.objects.get(user=request.user)
        exercises = user_content.my_exercises.all()
    except UserContent.DoesNotExist:
        exercises = []
    return render(request, 'content/my_exercises.html', {'exercises': exercises})


@login_required
def my_foods(request):
    try:
        user_content = UserContent.objects.get(user=request.user)
        foods = user_content.my_foods.all()
    except UserContent.DoesNotExist:
        foods = []
    return render(request, 'content/my_foods.html', {'foods': foods})


@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)

    if request.method == 'POST':
        exercise.name = request.POST.get('name')
        exercise.duration = request.POST.get('duration_min')
        exercise.calories_burned = request.POST.get('calories_burned')
        exercise.save()
        return redirect('exercise_detail', pk=exercise.pk)

    return render(request, 'content/exercise_detail.html', {'exercise': exercise})


@login_required
def add_exercise(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = request.POST.get('duration_min')
        calories = request.POST.get('calories_burned')

        exercise = Exercise.objects.create(
            user=request.user,
            name=name,
            duration_min=int(duration),
            calories_burned=int(calories)
        )

        user_content, created = UserContent.objects.get_or_create(user=request.user)

        user_content.my_exercises.add(exercise)

        return redirect('my_exercises')
    return render(request, 'content/add_exercise.html')


@login_required
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)

    serving_weight = food.serving_sizes or 100

    nutrition_fields = [
        ("Calories (kcal)", "calories", "label-blue"),
        ("Fat (g)", "fat", "label-yellow"),
        ("Saturated (g)", "saturated", ""),
        ("Polyunsaturated (g)", "polyunsaturated", ""),
        ("Monounsaturated (g)", "monounsaturated", ""),
        ("Trans (g)", "trans", ""),
        ("Cholesterol (mg)", "cholesterol", ""),
        ("Salt (g)", "salt", ""),
        ("Sodium (mg)", "sodium", ""),
        ("Potassium (mg)", "potassium", ""),
        ("Carbohydrate (g)", "carbohydrate", "label-red"),
        ("Dietary fiber (g)", "dietary_fiber", ""),
        ("Sugars (g)", "sugars", ""),
        ("Protein (g)", "protein", "label-blue"),
        ("Vitamin A (mg)", "vitamin_a", ""),
        ("Vitamin C (mg)", "vitamin_c", ""),
        ("Calcium (mg)", "calcium", ""),
        ("Iron (mg)", "iron", ""),
        ("Magnesium (mg)", "magnesium", ""),
    ]

    nutrition_data = []
    for label, field, css_class in nutrition_fields:
        val100 = getattr(food, field, 0) or 0
        try:
            val100 = float(val100)
        except (ValueError, TypeError):
            val100 = 0
        val_total = round(val100 * serving_weight / 100, 2)
        nutrition_data.append({
            "label": label,
            "val100": val100,
            "val_total": val_total,
            "css_class": css_class
        })

    return render(request, "content/food_detail.html", {
        "food": food,
        "nutrition_data": nutrition_data,
    })


def food_edit(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_detail', pk=food.pk)
    else:
        form = FoodForm(instance=food)

    return render(request, 'content/food_edit.html', {'form': form, 'food': food})


@require_POST
def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    food.delete()
    return redirect('my_foods')


@login_required
def add_food(request):
    settings = UserSettings.objects.get(user=request.user)
    energy_unit_label = "Calories (kj)" if settings.energy_unit == "kj" else "Calories (kcal)"
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()

            user_content, created = UserContent.objects.get_or_create(user=request.user)
            user_content.my_foods.add(food)

            return redirect('my_foods')
    else:
        form = FoodForm()

    return render(request, 'content/add_food.html', {'form': form, 'energy_unit_label': energy_unit_label})


# TODO --->
@login_required
def my_recipes(request):
    try:
        user_content = UserContent.objects.get(user=request.user)
        recipes = user_content.my_recipes.all()
    except UserContent.DoesNotExist:
        recipes = []
    return render(request, 'content/my_recipes.html', {'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    ingredients = recipe.ingredients.all()

    return render(request, "content/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
    })



@login_required
def add_recipe(request):
    settings = UserSettings.objects.get(user=request.user)
    energy_unit_label = "Calories (kj)" if settings.energy_unit == "kj" else "Calories (kcal)"
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()

            user_content, created = UserContent.objects.get_or_create(user=request.user)
            user_content.my_recipes.add(recipe)

            return redirect('my_recipes')
    else:
        form = RecipeForm()

    return render(request, 'content/add_recipe.html', {'form': form, 'energy_unit_label': energy_unit_label})



@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'content/recipe_edit.html', {'form': form, 'recipe': recipe})


@require_POST
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('my_recipes')


# TODO --->
@login_required
def my_goals(request):
    return render(request, 'content/my_goals.html')
