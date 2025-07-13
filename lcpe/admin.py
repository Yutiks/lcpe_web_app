from django.contrib import admin
from accounts.models import CustomUser, UserProfile, UserSettings
from food.models import Food
from training.models.exercise_session import Exercise
from content.models import UserContent
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'height_cm', 'weight_kg', 'activity_level', 'goal')
    list_filter = ('gender', 'activity_level', 'goal')
    search_fields = ('user__username', 'user__email')


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'height_unit', 'weight_unit', 'energy_unit', 'language', 'timezone')
    list_filter = ('height_unit', 'weight_unit', 'energy_unit', 'language', 'timezone')
    search_fields = ('user__username', 'user__email')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('description', 'brand', 'calories', 'fat', 'carbohydrate', 'protein')
    search_fields = ('description', 'brand', 'barcode')
    list_filter = ('brand',)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_min', 'calories_burned')
    search_fields = ('name',)


@admin.register(UserContent)
class UserContentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('my_foods', 'my_exercises')
