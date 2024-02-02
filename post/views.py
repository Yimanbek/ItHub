from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from ithub.tasks import send_comment_notification_tasks
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        post = Post.objects.create(title=title, content=content, author=author)
        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
    return render(request, 'create_post.html')
    
@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.create(post=post, content=content, author=author)
        if comment:
            send_comment_notification_tasks(post_id,content,author)
        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
    return HttpResponseRedirect(reverse('index'))




