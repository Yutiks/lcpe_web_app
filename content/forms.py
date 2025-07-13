from django import forms
from food.models import Food, Recipe


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ['user']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'serving_sizes': forms.TextInput(attrs={'class': 'form-control'}),

            'calories': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'saturated': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'polyunsaturated': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monounsaturated': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'trans': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'cholesterol': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salt': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sodium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'potassium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'carbohydrate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dietary_fiber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sugars': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'vitamin_a': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vitamin_c': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'calcium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'iron': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'magnesium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'by_serving_of': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'required': True}),
            'measurement_unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'directions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
