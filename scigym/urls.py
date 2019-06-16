from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .users.views import UserViewSet, UserCreateViewSet
from .repositories.views import RepositoryViewSet
from .config.views import app_config, image_config, index
from .environments.views import EnvironmentViewSet, TopicViewSet
from .contributors.views import ContributorViewSet
from .images.views import ImageViewSet

if settings.DEBUG is True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('users', UserCreateViewSet)
router.register('repositories', RepositoryViewSet)
router.register('environments', EnvironmentViewSet)
router.register('contributors', ContributorViewSet)
router.register('topics', TopicViewSet)
router.register('images', ImageViewSet)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/watchman/', include('watchman.urls')),
    path('api/v1/auth/', include('rest_framework_social_oauth2.urls')),
    path('api/v1/app_config/', app_config),
    path('api/v1/image_config/', image_config),
    path('api/v1/', include(router.urls)),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^/api$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is True:
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    path('', index, {'resource': ''}),
    path('<path:resource>', index)
]
