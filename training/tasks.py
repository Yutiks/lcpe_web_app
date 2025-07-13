from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models.training_plan import TrainingWeek
import pytz
from django.db.models import F
from django.core.mail import send_mail

MESSAGES = {
    'ru': {
        'subject': 'Напоминание о тренировке',
        'message': 'Привет, {username}! Не забудь про тренировку сегодня!',
    },
    'en': {
        'subject': 'Training Reminder',
        'message': 'Hi, {username}! Don\'t forget about your training today!',
    }
}

@shared_task
def send_training_reminders():
    print("Задача send_training_reminders запущена!")
    now_utc = timezone.now()
    today_weekday = now_utc.strftime('%A').lower()

    weeks = TrainingWeek.objects.select_related(
        'plan', 'plan__user', 'plan__user__usersettings', 'plan__user__usernotificationsettings'
    ).filter(
        week_number=F('plan__current_week')
    )

    for week in weeks:
        session = getattr(week, today_weekday)
        session_time = getattr(week, f"{today_weekday}_time")

        if session and session_time:
            user = week.plan.user
            notif_settings = getattr(user, 'usernotificationsettings', None)

            if not notif_settings or not notif_settings.email_notifications:  #TODO сделать чтобы настройки всегда были
                continue

            minutes_before = notif_settings.reminder_lead_time

            user_tz = user.usersettings.timezone or 'UTC'
            user_lang = getattr(user.usersettings, 'language', 'en')
            tz = pytz.timezone(user_tz)

            now_user = timezone.localtime(now_utc, tz)
            session_datetime = now_user.replace(
                hour=session_time.hour, minute=session_time.minute,
                second=0, microsecond=0
            )

            delta = session_datetime - now_user

            if timedelta(minutes=0) <= delta <= timedelta(minutes=minutes_before):
                msg = MESSAGES.get(user_lang, MESSAGES['en'])

                send_mail(
                    subject=msg['subject'],
                    message=msg['message'].format(username=user.username),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                minutes_until = int(delta.total_seconds() // 60)
                print(f"Напоминание отправлено: {user.username} | {minutes_until} мин. до тренировки | Язык: {user_lang}")
