from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Food, Meal, MealEntry, Recipe, MealItem
from content.models import UserContent
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

def customize_meals(request):
    meals = Meal.objects.filter(user=request.user).order_by('id')
    return render(request, 'food/customize_meals.html', {'meals': meals})


def add_meal(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Meal.objects.create(user=request.user, name=name)
            return redirect('customize_meals')
        else:
            error = "Please enter a meal name."
            return render(request, 'add_meal.html', {'error': error, 'name': name})

    return render(request, 'food/add_meal.html')


def meal_detail(request):
    return render(request, 'food/meal_detail.html')


def meal_entry_add_food(request, entry_id):
    user_content, _ = UserContent.objects.get_or_create(user=request.user)

    tab = request.GET.get("tab", "my_food")
    query = request.GET.get("search", "").strip()
    date = request.GET.get("date")

    if tab == "my_food":
        results = user_content.my_foods.all()
        if query:
            results = results.filter(description__icontains=query)

    elif tab == "my_recipes":
        results = user_content.my_recipes.all()
        if query:
            results = results.filter(description__icontains=query)

    elif tab == "library":
        # только продукты без владельца
        results = Food.objects.filter(user__isnull=True)
        if query:
            results = results.filter(description__icontains=query)
    else:
        results = []

    return render(request, "food/meal_entry_add_food.html", {
        "entry_id": entry_id,
        "tab": tab,
        "results": results,
        "query": query,
        "date": date,
    })


# @login_required
# @require_POST
# def add_food_to_entry(request, entry_id):
#     food_id = request.POST.get('food_id')
#     date = request.POST.get('date')
#     parsed_date = datetime.strptime(date, '%B %d, %Y')
#     date = parsed_date.strftime('%Y-%m-%d')
#     if food_id:
#         meal_entry = get_object_or_404(MealEntry, id=entry_id)
#         food = get_object_or_404(Food, id=food_id)
#         meal_entry.foods.add(food)
#         meal_entry.save()
#         if date:
#             return redirect(f'/diary/?date={date}')
#     return redirect('diary')
@login_required
@require_POST
def add_food_to_entry(request, entry_id):
    meal_entry = get_object_or_404(MealEntry, pk=entry_id)

    value = request.POST.get("add_item")
    date = request.POST.get("date")

    if date:
        try:
            parsed_date = datetime.strptime(date, '%B %d, %Y')
            formatted_date = parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            formatted_date = None
    else:
        formatted_date = None

    try:
        object_id, content_type_id = map(int, value.split("-"))
    except (ValueError, TypeError, AttributeError):
        return redirect("meal_entry_add_food", entry_id=entry_id)

    content_type = get_object_or_404(ContentType, pk=content_type_id)
    model_class = content_type.model_class()
    obj = get_object_or_404(model_class, pk=object_id)

    MealItem.objects.create(
        meal_entry=meal_entry,
        content_type=content_type,
        object_id=obj.id,
        amount=1.0,
    )

    if formatted_date:
        return redirect(f"/diary/?date={formatted_date}")
    return redirect("diary")



@login_required
@require_POST
def meal_entry_remove_food(request, entry_id, food_id):
    entry = get_object_or_404(
        MealEntry.objects.filter(daily_logs__user=request.user).distinct(),
        id=entry_id
    )

    food_ct = ContentType.objects.get_for_model(Food)

    MealItem.objects.filter(
        meal_entry=entry,
        content_type=food_ct,
        object_id=food_id
    ).delete()

    date = request.POST.get('date')
    if date:
        try:
            parsed_date = datetime.strptime(date, '%B %d, %Y')
            return redirect(f'/diary/?date={parsed_date.strftime("%Y-%m-%d")}')
        except ValueError:
            pass

    return redirect('diary')


def set_meal_time(request):
    return render(request, 'meal_detail.html')  # ffff


def meal_entry_food_library(request):
    return render(request, 'meal_detail.html')  # ffff


def meal_entry_my_recipes(request):
    return render(request, 'meal_detail.html')  # ffff


def meal_entry_my_food(request):
    return render(request, 'meal_detail.html')  # ffff
