

from django.contrib import admin
from django.urls import path, include
from accounts.views import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('admin/', admin.site.urls),
    path('', include('boards.urls')),
]
