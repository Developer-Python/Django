# импортируем Админку
from django.contrib import admin
# импортируем функцию path и include для работы с путями
from django.urls import path, include
# импортируем настройки приложений
from django.conf import settings
# импортируем функцию static для работы с путями статических файлов(изображения, архивы, торренты,иконки и т.д)
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
