from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from bc import urls, views

urlpatterns = [
    path('swagger/', views.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(urls.urlpatterns)),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/auth/login/', views.login_access),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/profile/', views.redirect_to_note, name='redirect-to-note'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view())
]


