from django.urls import path
from . import views

urlpatterns = [
    path("customize-meals/", views.customize_meals, name="customize_meals"),
    path("customize-meals/add/", views.add_meal, name="add_meal"),
    path("customize-meals/<int:pk>/", views.meal_detail, name="meal_detail"),
    # meal_entry запись в дневнике
    path('set_meal_time/<int:entry_id>/', views.set_meal_time, name='set_meal_time'),
    path('meal_entry_add_food/<int:entry_id>/', views.meal_entry_add_food, name='meal_entry_add_food'),
    path('meal_entry_add_food/<int:entry_id>/my_food/', views.meal_entry_my_food, name='my_food'),
    path('meal_entry_add_food/<int:entry_id>/my_recipes/', views.meal_entry_my_recipes, name='my_recipes'),
    path('meal_entry_add_food/<int:entry_id>/food_library/', views.meal_entry_food_library, name='food_library'),
    path('meal_entry_add_food/<int:entry_id>/add-food/', views.add_food_to_entry, name='add_food_to_entry'),
    path('meal_entry/<int:entry_id>/remove-food/<int:food_id>/', views.meal_entry_remove_food, name='meal_entry_remove_food'),

]
