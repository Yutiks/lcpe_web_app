from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_web, name='settings'),
    path('settings/language_and_timezone/', views.set_language_and_timezone, name='set_language_and_timezone'),
    path('settings/formula', views.formula, name='formula'),
    path('settings/notification_preferences', views.notification_preferences, name='notification_preferences'),
    path('settings/Units_and_formats', views.units_and_formats, name='Units_and_formats'),
    path('settings/notification_preferences/update/', views.update_notification_setting, name='update_notification_setting'),
]
