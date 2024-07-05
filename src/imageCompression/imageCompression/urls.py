from django.contrib import admin
from django.urls import path, include

import compression.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(compression.urls)),
]
