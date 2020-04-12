from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500 # noqa, pylint: disable=unused-import
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as v

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
        path("admin/", admin.site.urls),
        path("about/", include("django.contrib.flatpages.urls")),
        # path("auth/", include("users.urls")),
        # path("auth/", include("django.contrib.auth.urls")),
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('api-token-auth/', v.obtain_auth_token),
        path('api/v1/', include('api.urls')),
        path("", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
