
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
# Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
    path('news/', include('news_portal.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += i18n_patterns(
    path('',  include('news_portal.urls')),
)
