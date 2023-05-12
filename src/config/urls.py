"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.network import views
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', views.Index.as_view()),
    path('admin/', admin.site.urls),
    # path('confirm/', views.ConfirmUser.as_view()),
    path('register/', views.CreateUser.as_view()),
    path('token/', obtain_auth_token),

    path('friendship/<username>/', views.FriendAPIView.as_view()),

    path('requests/out/', views.OutgoingRequestAPIView.as_view()),
    path('requests/in/', views.IncomingRequestAPIView.as_view()),
    path('requests/accepted/', views.AcceptedRequestAPIView.as_view()),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
