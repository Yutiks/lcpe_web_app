from django import forms
from .models.training_session import TrainingSession
from .models.exercise_session import ExerciseSession
from .models.training_plan import TrainingWeek, TrainingPlan


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['name', 'completion']
        widgets = {
            'completion': forms.Textarea(attrs={'rows': 4}),
        }


class ExerciseSessionForm(forms.ModelForm):
    class Meta:
        model = ExerciseSession
        fields = ['exercise_name', 'sets', 'reps', 'percentage_1rm']
        widgets = {
            'exercise_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Barbell Squat'
            }),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'percentage_1rm': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': 'e.g. 80'
            }),
        }
        labels = {
            'exercise_name': 'Exercise Name',
            'sets': 'Sets',
            'reps': 'Reps per Set',
            'percentage_1rm': 'Percentage of 1RM',
        }


DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
]


class TrainingWeekForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        sessions = TrainingSession.objects.filter(user=user)

        for day in DAYS:
            # Поле-сессия
            fld = self.fields[day]
            fld.queryset = sessions
            fld.label = day.capitalize()
            fld.required = False                   # необязательно
            fld.empty_label = ' '                  # дефолтный пустой выбор

            # Поле-время
            time_fld = self.fields[f"{day}_time"]
            time_fld.widget = forms.TimeInput(attrs={'type': 'time'})
            time_fld.required = False              # тоже необязательно

        # Если неделю не хотим редактировать вручную, можно скрыть:
        self.fields['week_number'].widget = forms.HiddenInput()

    class Meta:
        model = TrainingWeek
        fields = [
            'week_number',
            *DAYS,
            *[f"{day}_time" for day in DAYS],
        ]


