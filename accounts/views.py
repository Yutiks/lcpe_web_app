import json

from django.conf import settings
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import translation
from django.utils.timezone import activate as activate_timezone
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile, UserSettings, UserNotificationSettings
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render
from django.contrib import messages


def cm_to_ft_in(cm):
    inches = cm / 2.54
    feet = int(inches // 12)
    inch = round(inches % 12)
    return feet, inch


def ft_in_to_cm(feet, inches):
    return round((feet * 12 + inches) * 2.54)


def kg_to_lbs(kg):
    return round(kg * 2.20462, 1)


def lbs_to_kg(lbs):
    return round(lbs / 2.20462, 1)


def ml_to_oz(ml):
    return round(ml / 29.5735, 1)


def oz_to_ml(oz):
    return round(oz * 29.5735, 1)


def ml_to_cups(ml):
    return round(ml / 240, 1)


def cups_to_ml(cups):
    return round(cups * 240)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        verification = authenticate(request, username=username, password=password)
        if verification:
            login_django(request, verification)
            return redirect("home_page")
    return render(request, "accounts/login.html")


def registration(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_django(request, user)
            return redirect("home_page")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", context={"form": form})


@login_required
def profile(request):
    user = request.user
    pr4e, _ = UserProfile.objects.get_or_create(user=user)
    user_settings, _ = UserSettings.objects.get_or_create(user=user)

    if request.method == 'GET':
        height_display = pr4e.height_cm
        weight_display = pr4e.weight_kg

        if user_settings.height_unit == 'ft_in' and pr4e.height_cm:
            ft, inch = cm_to_ft_in(pr4e.height_cm)
            height_display = {'feet': ft, 'inches': inch}

        if user_settings.weight_unit == 'lbs' and pr4e.weight_kg:
            weight_display = kg_to_lbs(pr4e.weight_kg)

        form = UserProfileForm(instance=pr4e)
        return render(request, 'accounts/profile.html', {
            'form': form,
            'user_settings': user_settings,
            'height_display': height_display,
            'weight_display': weight_display
        })

    elif request.method == 'POST':
        data = request.POST.copy()

        if user_settings.height_unit == 'ft_in':
            try:
                ft = int(request.POST.get('height_ft', 0))
                inch = int(request.POST.get('height_in', 0))
                data['height_cm'] = ft_in_to_cm(ft, inch)
            except (ValueError, TypeError):
                data['height_cm'] = None

        if user_settings.weight_unit == 'lbs':
            try:
                lbs = float(request.POST.get('weight_lbs'))
                data['weight_kg'] = lbs_to_kg(lbs)
            except (ValueError, TypeError):
                data['weight_kg'] = None

        form = UserProfileForm(data, instance=pr4e)

        if form.is_valid():
            form.save()
            return redirect('home_page')

        height_display = {
            'feet': request.POST.get('height_ft', ''),
            'inches': request.POST.get('height_in', '')
        } if user_settings.height_unit == 'ft_in' else data.get('height_cm')

        weight_display = request.POST.get('weight_lbs', '') if user_settings.weight_unit == 'lbs' else data.get(
            'weight_kg', '')

        return render(request, 'accounts/profile.html', {
            'form': form,
            'user_settings': user_settings,
            'height_display': height_display,
            'weight_display': weight_display
        })


@login_required
def logout(request):
    logout_django(request)
    return redirect("login")


@login_required
def set_language_and_timezone(request):
    user = request.user
    settings_obj, _ = UserSettings.objects.get_or_create(user=user)

    if request.method == 'POST':
        lang = request.POST.get('language')
        tz = request.POST.get('timezone')

        if lang:
            settings_obj.language = lang
            request.session['django_language'] = lang
            translation.activate(lang)
            response = redirect('settings')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        else:
            response = redirect('settings')

        if tz:
            settings_obj.timezone = tz
            request.session['django_timezone'] = tz
            activate_timezone(tz)

        settings_obj.save()
        return response

    return render(request, 'accounts/set_language_and_timezone.html', {
        'timezones': dict(UserSettings.TIMEZONES),  # если ты хочешь с описаниями
        'current': settings_obj
    })


@login_required
def formula(request):
    user = request.user
    settings_obj, _ = UserSettings.objects.get_or_create(user=user)
    pr4e = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        selected_formula = request.POST.get('formula')
        fat_percentage = request.POST.get('fat_percentage')

        if selected_formula:
            settings_obj.formula = selected_formula

            if selected_formula == 'katch_mcardle':
                if not fat_percentage:
                    messages.error(request, "Fat percentage is required for Katch-McArdle.")
                    return redirect('formula')
                try:
                    pr4e.fat_percentage = float(fat_percentage)
                except ValueError:
                    messages.error(request, "Fat percentage must be a number.")
                    return redirect('formula')
            else:
                pr4e.fat_percentage = None

            settings_obj.save()
            pr4e.save()

        return redirect('settings')

    return render(request, 'accounts/formula.html', {
        'formulas': dict(UserSettings.FORMULAS),
        'selected_formula': settings_obj.formula,
        'fat_percentage': pr4e.fat_percentage,
    })


@login_required
def units_and_formats(request):
    user = request.user
    user_settings, _ = UserSettings.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_settings.height_unit = request.POST.get('height_unit')
        user_settings.weight_unit = request.POST.get('weight_unit')
        user_settings.energy_unit = request.POST.get('energy_unit')
        user_settings.water_unit = request.POST.get('water_unit')

        user_settings.date_format = request.POST.get('date_format')
        user_settings.time_format = request.POST.get('time_format')
        user_settings.week_start = request.POST.get('week_start')

        user_settings.save()
        return redirect('settings')

    return render(request, 'accounts/units_and_formats.html', {
        'user_settings': user_settings,
        'height_units': UserSettings.HEIGHT_UNITS,
        'weight_units': UserSettings.WEIGHT_UNITS,
        'energy_units': UserSettings.ENERGY_UNITS,
        'water_units': UserSettings.WATER_UNITS,
        'date_formats': UserSettings.DATE_FORMATS,
        'time_formats': UserSettings.TIME_FORMATS,
        'week_starts': UserSettings.WEEK_STARTS,
    })


@login_required
def settings_web(request):
    return render(request, 'accounts/settings.html')


# TODO ---->
@login_required
def notification_preferences(request):
    sett, created = UserNotificationSettings.objects.get_or_create(user=request.user)
    minutes = [5, 10, 15, 30]
    return render(request, 'accounts/notification_preferences.html', {'settings': sett, "minutes": minutes})


@csrf_exempt
def update_notification_setting(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        sett, created = UserNotificationSettings.objects.get_or_create(user=request.user)

        if hasattr(sett, field):
            setattr(sett, field, value)
            sett.save()
            return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'}, status=400)
