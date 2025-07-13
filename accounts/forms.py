from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height_cm', 'weight_kg', 'gender', 'age', 'activity_level', 'goal']
        labels = {
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',
            'gender': 'Gender',
            'age': 'Age',
            'activity_level': 'Activity Level',
            'goal': 'Goal',
        }
