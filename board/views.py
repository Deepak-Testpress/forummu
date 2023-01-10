from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Board, Topic, Post
from .forms import NewTopicForm, NewPostForm, CreateBoardForm, EditPostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404

def home(request):
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})


def board_topics(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, "topics.html", {"board": board, "topics": topics})

@login_required
def new_topic(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    user = request.user
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=user,
            )
            return redirect("board_topics", board_id=board.id)
    else:
        form = NewTopicForm()

    return render(request, "new_topic.html", {"board": board, "form": form})


def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__id=board_id, id=topic_id)
    topic.views += 1
    topic.save()
    return render(request, "topic_posts.html", {"topic": topic})

@login_required
def add_post(request, board_id, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    user = request.user

    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=user,
            )
            return redirect("topic_posts", board_id=board_id, topic_id=topic_id)
    else:
        form = NewPostForm()

    return render(request, "add_post.html", {"topic": topic})

@login_required
def edit_post(request, board_id, topic_id, post_id):
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    topic = get_object_or_404(Topic, id=topic_id)
    form = EditPostForm(request.POST or None, instance=post)
    if form.is_valid():
        post.message = form.cleaned_data.get("message")
        post.updated_at = timezone.now()
        post.updated_by = request.user
        post.save()
        return redirect("topic_posts", board_id=board_id, topic_id=topic_id)
    return render(request, "edit_post.html", {"topic": topic, "form":form})

def create_board(request):
    if request.method == "POST":
        form = CreateBoardForm(request.POST)
        if form.is_valid():
            Board.objects.create(
                name=form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
            )
            return redirect("home")
    return render(request, "create_board.html")
