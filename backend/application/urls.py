from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from system.auth import Login, Captcha, PublicConfig, PublicConfigValues, Account, Password, FirstPassword
from system.views import Metadata, Inbox, DictionaryData, view_for
from system.catalog import ENTITIES
from system.events import MessageEvents
from .plugins import URLS
from core.health import healthz, readiness

router = DefaultRouter()
for entity, model in ENTITIES.items():
    router.register(entity, view_for(entity, model), basename=entity)

urlpatterns = [
    path('healthz', healthz), path('readiness', readiness),
    path('api/login/', Login.as_view()), path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/captcha/', Captcha.as_view()), path('captcha/', include('captcha.urls')),
    path('api/config/', PublicConfig.as_view()), path('api/account/', Account.as_view()),
    path('api/config/values/', PublicConfigValues.as_view()),
    path('api/password/', Password.as_view()), path('api/inbox/', Inbox.as_view()),
    path('api/password/first/', FirstPassword.as_view()),
    path('api/events/', MessageEvents.as_view()),
    path('api/dictionary/', DictionaryData.as_view()),
    path('api/meta/<str:entity>/', Metadata.as_view()), path('api/system/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path(f'api/plugins/{name}/', include(urls)) for name, urls in URLS]
urlpatterns += [re_path(r'^(?!api/|media/|captcha/|static/).*$', TemplateView.as_view(template_name='index.html'))]
