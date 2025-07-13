from django.shortcuts import render
from .models import CSAI2Result, SCATResult, POMSResult, TEOSQResult
from .forms import SCATForm, CSAI2Form, POMSForm, TEOSQForm


def scat_test(request):
    score = None
    interpretation = ""
    past_results = []

    if request.method == 'POST':
        form = SCATForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            total = sum(int(value) for key, value in cleaned.items() if key != 'notes')
            score = total

            if score <= 10:
                interpretation = "Low level of anxiety"
            elif score <= 20:
                interpretation = "Moderate level of anxiety"
            else:
                interpretation = "High level of anxiety"

            if request.user.is_authenticated:
                SCATResult.objects.create(
                    user=request.user,
                    score=score,
                    interpretation=interpretation,
                    notes=cleaned.get('notes', '')
                )
    else:
        form = SCATForm()

    if request.user.is_authenticated:
        past_results = SCATResult.objects.filter(user=request.user).order_by('-date')

    return render(request, 'psychology/scat_test.html', {
        'form': form,
        'score': score,
        'interpretation': interpretation,
        'past_results': past_results,
    })


def csai2_test(request):
    scores = {}
    past_results = []

    if request.method == 'POST':
        form = CSAI2Form(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            data = {k: int(v) for k, v in cleaned.items() if k != 'notes'}

            cognitive = sum([data[q] for q in ['q1', 'q5', 'q8', 'q11', 'q14', 'q17']])
            somatic = sum([data[q] for q in ['q2', 'q4', 'q6', 'q9', 'q12', 'q15', 'q18']])
            confidence = sum([data[q] for q in ['q3', 'q7', 'q10', 'q13', 'q16', 'q19']])

            scores = {
                'cognitive': cognitive,
                'somatic': somatic,
                'confidence': confidence,
            }

            if request.user.is_authenticated:
                CSAI2Result.objects.create(
                    user=request.user,
                    cognitive_score=cognitive,
                    somatic_score=somatic,
                    confidence_score=confidence,
                    notes=cleaned.get('notes', '')
                )

    else:
        form = CSAI2Form()

    if request.user.is_authenticated:
        past_results = CSAI2Result.objects.filter(user=request.user).order_by('-date')

    return render(request, 'psychology/csai2_test.html', {
        'form': form,
        'scores': scores,
        'past_results': past_results,
    })


def poms_test(request):
    scores = {}
    past_results = []

    if request.method == 'POST':
        form = POMSForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            data = {k: int(v) for k, v in cleaned.items() if k != 'notes'}
            tension = sum([int(data[q]) for q in ['tense', 'anxious', 'nervous']])
            depression = sum([int(data[q]) for q in ['depressed', 'unhappy', 'discouraged', 'gloomy', 'lonely']])
            anger = int(data['angry'])
            vigor = sum([int(data[q]) for q in ['vigorous', 'energetic', 'energetic_2', 'lively', 'cheerful', 'cheerful_2', 'friendly', 'calm']])
            fatigue = sum([int(data[q]) for q in ['fatigued', 'sleepy', 'weak', 'restless', 'impatient']])
            confusion = sum([int(data[q]) for q in ['confused', 'confused_2']])

            scores = {
                'tension': tension,
                'depression': depression,
                'anger': anger,
                'vigor': vigor,
                'fatigue': fatigue,
                'confusion': confusion,
            }

            if request.user.is_authenticated:
                POMSResult.objects.create(
                    user=request.user,
                    tension_score=tension,
                    depression_score=depression,
                    anger_score=anger,
                    vigor_score=vigor,
                    fatigue_score=fatigue,
                    confusion_score=confusion,
                    notes=cleaned.get('notes', '')
                )
    else:
        form = POMSForm()

    if request.user.is_authenticated:
        past_results = POMSResult.objects.filter(user=request.user).order_by('-date')

    return render(request, 'psychology/poms_test.html', {
        'form': form,
        'scores': scores,
        'past_results': past_results,
    })


def teosq_test(request):
    task_score = None
    ego_score = None
    dominant_type = ""
    past_results = []

    if request.method == 'POST':
        form = TEOSQForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            task_items = ['q2', 'q5', 'q7', 'q8', 'q10', 'q12', 'q13']
            ego_items = ['q1', 'q3', 'q4', 'q6', 'q9', 'q11']

            task_score = sum(cleaned[q] for q in task_items) // 7
            ego_score = sum(cleaned[q] for q in ego_items) // 6

            if task_score > ego_score:
                dominant_type = "Task-oriented"
            elif ego_score > task_score:
                dominant_type = "Ego-oriented"
            else:
                dominant_type = "Balanced"

            if request.user.is_authenticated:
                TEOSQResult.objects.create(
                    user=request.user,
                    task_orientation=task_score,
                    ego_orientation=ego_score,
                    dominant_type=dominant_type,
                    notes=cleaned.get('notes', '')
                )
    else:
        form = TEOSQForm()

    if request.user.is_authenticated:
        past_results = TEOSQResult.objects.filter(user=request.user).order_by('-date')

    return render(request, 'psychology/teosq_test.html', {
        'form': form,
        'task_score': task_score,
        'ego_score': ego_score,
        'dominant_type': dominant_type,
        'past_results': past_results,
    })
