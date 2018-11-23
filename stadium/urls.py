from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .users.views import UserViewSet, UserCreateViewSet
from .repos.views import RepoViewSet
from .config.views import app_config

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('users', UserCreateViewSet)
router.register('repos', RepoViewSet)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/watchman/', include('watchman.urls')),
    path('api/auth/', include('rest_framework_social_oauth2.urls')),
    path('api/v1/app_config/', app_config),
    path('api/v1/', include(router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^/api$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
