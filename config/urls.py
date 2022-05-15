
from django.contrib import admin
from django.urls import path, include

import movies.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', movies.views.base)
]
