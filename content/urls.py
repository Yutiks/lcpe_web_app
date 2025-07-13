from django.urls import path
from . import views

urlpatterns = [
    path('my_exercises', views.my_exercises, name='my_exercises'),
    path('my_exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('my_exercises/add_exercise', views.add_exercise, name='add_exercise'),
    path('my_foods/', views.my_foods, name='my_foods'),
    path('my_foods/<int:pk>/', views.food_detail, name='food_detail'),
    path('my_foods/add_food', views.add_food, name='add_food'),
    path('my_foods/<int:pk>/edit/', views.food_edit, name='food_edit'),
    path('my_foods/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('my_recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('my_recipes/add_recipe', views.add_recipe, name='add_recipe'),
    path('my_recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('my_recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('my_goals/', views.my_goals, name='my_goals'),
]
