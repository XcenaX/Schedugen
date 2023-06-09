from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_yasg.inspectors import SwaggerAutoSchema

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="API Документация",
        default_version='v1',
        description="Тут описаны все url",        
        contact=openapi.Contact(email="vladleb@inc.kz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[],
    authentication_classes=[],
    
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Получение JWT-токена    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    # Обновление JWT-токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Добавьте ваши собственные пути для вашего API

    path('admin/', admin.site.urls),     
    path('api/', include('main.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)