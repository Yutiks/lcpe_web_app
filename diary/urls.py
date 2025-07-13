from django.urls import path
from . import views

urlpatterns = [
    path('', views.diary, name='diary'),
    path('settings/', views.settings_diary, name='settings_diary'),
    path('settings/update/', views.update_diary_setting, name='update_diary_setting'),
    path('update_water/<str:direction>/', views.update_water, name='update_water'),
    path('add_exercise/', views.add_exercise_to_diary, name='add_exercise_to_diary'),
    path('add_exercise/submit/', views.add_exercise_to_log, name='add_exercise_to_log'),
    path('exercise/remove/<int:exercise_id>/', views.remove_exercise, name='remove_exercise'),
]
