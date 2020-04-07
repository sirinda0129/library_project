from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as v

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
        # раздел администратора
        path("admin/", admin.site.urls),
        # flatpages
        path("about/", include("django.contrib.flatpages.urls")),
        # регистрация и авторизация
        path("auth/", include("users.urls")),
        path("auth/", include("django.contrib.auth.urls")),
        # импорт из приложения posts
        path("", include("posts.urls")),
]

urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('api-token-auth/', v.obtain_auth_token),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)