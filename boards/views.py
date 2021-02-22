from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post, Topic
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# def home(request):
#     boards = Board.objects.all()
#     return render(request, 'home.html', locals())


class BoardsListView(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
#     return render(request, 'topics.html', locals())


class BoardDetailTopicListView(DetailView):
    model = Board
    template_name = 'topics.html'
    context_object_name = 'board' # Board.objects.get(pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = self.get_object().topics.order_by('-last_updated').annotate(replies=Count('posts'))
        return context


# @login_required
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         form = NewTopicForm(request.POST)
#         if form.is_valid(): 
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             post = Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 topic=topic,
#                 created_by=request.user
#             )
#             return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
#     else:
#         form = NewTopicForm()
#     return render(request, 'new_topic.html', locals())


class NewTopicView(CreateView, LoginRequiredMixin):
    model = Topic
    template_name = 'new_topic.html'
    form_class = NewTopicForm
    context_object_name = 'form' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        board_pk =  Board.objects.get(pk=self.kwargs.get('pk'))
        topic.board =board_pk
        topic.starter = self.request.user
        topic.save()
        post = Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=self.request.user
        )
        return redirect('topic_posts', pk=board_pk, topic_pk=topic.pk)


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', locals()) # {'posts}: posts


class PostListView(ListView):
    model = Post
    context_object_name = 'posts' # Post.objects.all()
    template_name = 'topic_posts.html'
    paginate_by = 4

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        self.topic.views += 1
        self.topic.save()
        return context
    

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', locals())



class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    context_object_name = 'post'
    fields = ('message', )
    pk_url_kwarg = 'post_pk'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


# def new_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'new_post.html', {})


# class NewPostView(View):
#     def render(self, request):
#         return render(request, 'new_post.html', {'form': form})

#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return self.render(request)

#     def get(self, request):
#         form = PostForm()
#         return self.render(request)





