from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view()),
    path("code-verification/", views.CodeVerificationAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("token-test/", views.TestTokenAPIView.as_view()),
    path("logout/", views.LogOutAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)