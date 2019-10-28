from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import HashTag, Post
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

def create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) # 사진의 경우 FIELS에 들어있음
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # save 가 실행되어야 post의 id가 부여가 된다
            # 즉 hastag와 연결을 할려면 post.save() 후에 해야한다.
            for word in post.content.split():
                if word.startswith('#') and len(word) > 2:
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    # get_or_create()는 (obj, bool)을 반환한다. get이 작동하면 False
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)

def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#') and len(word) > 2:
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    # get_or_create()는 (obj, bool)을 반환한다. get이 작동하면 False
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    context = {
        'form':form
    }
    return render(request, 'posts/form.html', context)


def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)

    posts = hashtag.taged_post.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)

def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:index')