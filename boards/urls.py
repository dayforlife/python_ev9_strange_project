from django.urls import path
# from boards import views
from .views import home, board_topics, new_topic


urlpatterns = [
    path('home/', home, name='home'),
    path('board/<int:pk>/', board_topics, name='board_topics'),
    path('board/<int:pk>/new/', new_topic, name='new_topic'),
]