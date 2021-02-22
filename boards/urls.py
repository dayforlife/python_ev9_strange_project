from django.urls import path
from .views import (reply_topic,
                    BoardsListView, BoardDetailTopicListView,
                    NewTopicView, PostListView, EditPostView)



urlpatterns = [
    # path('home/', home, name='home'),
    path('home/', BoardsListView.as_view(), name='home'),
    # path('board/<int:pk>/', board_topics, name='board_topics'),
    path('board/<int:pk>/', BoardDetailTopicListView.as_view(), name='board_topics'),
    # path('board/<int:pk>/new/', new_topic, name='new_topic'),
    path('board/<int:pk>/new/', NewTopicView.as_view(), name='new_topic'),

    # path('board/<int:pk>/<int:topic_pk>/', topic_posts, name='topic_posts'),
    path('board/<int:pk>/<int:topic_pk>/', PostListView.as_view(), name='topic_posts'),

    path('board/<int:pk>/topics/<int:topic_pk>/reply/', reply_topic, name='reply_topic'),
    path('board/<int:pk>/topics/<int:topic_pk>/<int:post_pk>/', EditPostView.as_view(), name='edit_post'),

    # path('new_post/', NewPostView.as_view(), name='new_post')
]