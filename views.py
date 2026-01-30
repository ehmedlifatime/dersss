from django.shortcuts import render
from django.db.models import Q 
from .models import Category, Post, Author, Comment, PostReport
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    post.views +=1
    post.save(update_fields=['views'])
    post.refresh_from_db()
    context = {
        'post': post,
        'latest': latest,
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

@login_required
def like_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)

        if request.user in post.likes.all():
            post.unlikes.remove(request.user)
        else:
            post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))
def unlike_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, id=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.unlikes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))

def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        body = request.POST.get('body')
        if body:
            Comment.objects.create(
                post=post,
                user=request.user,
                body=body
            )

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def favourite_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.favourites.all():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Eyni user eyni postu 2 dəfə report etməsin
    if not PostReport.objects.filter(post=post, user=request.user).exists():
        PostReport.objects.create(post=post, user=request.user)

    return redirect('post_view', post_id=post.id)
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {'post': post})