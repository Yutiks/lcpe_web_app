from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('content/', include('content.urls')),
    path('diary/', include('diary.urls')),
    path('food/', include('food.urls')),
    path('psychology/', include('psychology.urls')),
    path('training/', include('training.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
