from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='topics')

    def __str__(self):
        return f'{self.board} - {self.subject} by {self.starter}'


class Post(models.Model):
    message = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='create_posts')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                   related_name='update_posts')
    
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('created_at',)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='images')
    image = models.ImageField(upload_to='posts')