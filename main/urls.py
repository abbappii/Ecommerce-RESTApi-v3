from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from main.settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', obtain_auth_token),
    path('api/',include('shop.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += [ 
        path('', TemplateView.as_view(template_name = 'index.html')),
    ]

if not settings.DEBUG:
    urlpatterns +=[
        path('', TemplateView.as_view(template_name='index.html')),
    ]