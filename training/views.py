from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .models.training_session import TrainingSession
from .models.training_plan import TrainingWeek, TrainingPlan
from .models.fitness_test_results import FitnessTestResult
from psychology.models import CSAI2Result, SCATResult, POMSResult, TEOSQResult
from .forms import TrainingSessionForm, ExerciseSessionForm, TrainingWeekForm
from django.forms import modelformset_factory


@login_required
def tables(request):
    sessions = TrainingSession.objects.filter(user=request.user).prefetch_related('exercises')
    scat_results = SCATResult.objects.filter(user=request.user).order_by('-date')
    csai2_results = CSAI2Result.objects.filter(user=request.user).order_by('-date')
    poms_results = POMSResult.objects.filter(user=request.user).order_by('-date')
    teosq_results = TEOSQResult.objects.filter(user=request.user).order_by('-date')

    plan, _ = TrainingPlan.objects.get_or_create(user=request.user, defaults={'title': 'My Plan'})
    weeks = plan.weeks.order_by('week_number').prefetch_related(
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
    )

    fitness_results = FitnessTestResult.objects.filter(user=request.user)

    initial_results = {r.test_name: r.result for r in fitness_results if r.result_type == 'initial'}
    retest_results = {r.test_name: r.result for r in fitness_results if r.result_type == 'retest'}

    return render(request, 'training/tables.html', {
        'sessions': sessions,
        'scat_results': scat_results,
        'csai2_results': csai2_results,
        'poms_results': poms_results,
        'teosq_results': teosq_results,
        'plan': plan,
        'weeks': weeks,
        'initial_results': initial_results,
        'retest_results': retest_results,
    })


@login_required
def create_training_session(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('training_session_created', session_id=session.id)
    else:
        form = TrainingSessionForm()
    return render(request, 'training/create_training_session.html', {'form': form})


@login_required
def training_session_created(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id, user=request.user)
    return render(request, 'training/training_session_created.html', {'session': session})


@login_required
def add_session_exercise(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id, user=request.user)

    if request.method == 'POST':
        form = ExerciseSessionForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.training_session = session
            exercise.save()
            return redirect('add_session_exercise', session_id=session.id)
    else:
        form = ExerciseSessionForm()

    return render(request, 'training/add_exercise_session.html', {
        'form': form,
        'training_session': session
    })


@login_required
def list_sessions(request):
    sessions = TrainingSession.objects.filter(user=request.user)
    return render(request, 'training/select_session.html', {'sessions': sessions})


DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


@login_required
def edit_training_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id, user=request.user)

    existing = plan.weeks.count()
    for i in range(existing + 1, 7):
        TrainingWeek.objects.create(plan=plan, week_number=i)

    WeekFormSet = modelformset_factory(
        TrainingWeek,
        form=TrainingWeekForm,
        extra=0
    )
    qs = TrainingWeek.objects.filter(plan=plan).order_by('week_number').select_related(*DAYS)
    if request.method == 'POST':
        formset = WeekFormSet(request.POST, queryset=qs, form_kwargs={'user': request.user})
        if formset.is_valid():
            formset.save()
            return redirect('tables')
    else:
        formset = WeekFormSet(queryset=qs, form_kwargs={'user': request.user})

    return render(request, 'training/edit_training_plan.html', {
        'plan': plan,
        'formset': formset,
        'days': DAYS,
    })


TESTS = [
    "12 Minute Cooper Run",
    "Standing Broad Jump",
    "Sit and Reach",
    "Plank Hold",
    "1m Sit-up Test",
    "1m Press-up Test",
    "1m Squat Test",
    "Balance",
    "Wall/Ball Toss Test",
    "T-Test",
    "Vertical Jump Test",
    "Ruler Drop Test",
]


def edit_results(request):
    result_type = request.GET.get("type", "initial")
    user = request.user

    if request.method == "POST":
        for test_name in TESTS:
            field_name = f"result_{test_name}"
            result_value = request.POST.get(field_name)

            if result_value:
                obj, created = FitnessTestResult.objects.get_or_create(
                    user=user,
                    test_name=test_name,
                    result_type=result_type,
                    defaults={"component": "General"}
                )
                obj.result = result_value
                obj.save()
        return redirect("tables")

    results = FitnessTestResult.objects.filter(user=user, result_type=result_type)
    existing_results = {res.test_name: res.result for res in results}

    context = {
        "result_type": result_type,
        "tests": TESTS,
        "existing_results": existing_results,
    }
    return render(request, "training/edit_results.html", context)


@require_POST
@login_required
def update_current_week(request):
    try:
        week_number = int(request.POST.get('week_number'))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid week number")

    plan = TrainingPlan.objects.filter(user=request.user).first()
    if plan:
        plan.current_week = week_number
        plan.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
