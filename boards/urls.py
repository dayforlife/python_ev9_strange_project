from django.urls import path
# from boards import views
from .views import home


urlpatterns = [
    path('home/', home, name='home'),
]