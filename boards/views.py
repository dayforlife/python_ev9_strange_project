from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post
from .forms import NewTopicForm


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', locals())


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', locals())


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid(): 
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic = topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form=NewTopicForm()
    return render(request, 'new_topic.html', locals())