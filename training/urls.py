from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.tables, name='tables'),
    path('tables/training_sessions/create/', views.create_training_session, name='create_training_session'),
    path('tables/training_sessions/<int:session_id>/created/', views.training_session_created, name='training_session_created'),
    path('tables/training_sessions/list_sessions/', views.list_sessions, name='list_sessions'),
    path('tables/training_sessions/<int:session_id>/add_exercise/', views.add_session_exercise, name='add_session_exercise'),
    path('tables/training_plan/<int:plan_id>/edit/', views.edit_training_plan, name='edit_training_plan'),
    path('tables/edit_results/', views.edit_results, name='edit_results'),
    path('update_current_week/', views.update_current_week, name='update_current_week'),
]
