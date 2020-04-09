from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from pytils.translit import slugify
from .models import Post, Group, User
from .forms import PostForm, GroupForm


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {'group': group, 'page': page, 'paginator': paginator})

@login_required
def new_post(request):
    title = 'Опубликовать запись'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    form = PostForm()
    return render(request, "new_post.html", {"form": form, "title": title})

@login_required
def post_edit(request, post_id):
    title = 'Редактировать запись'
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post', post_id=post.pk)
        form = PostForm(instance=post)
    else:
        return redirect('post', post_id=post.pk)
    return render(request, "new_post.html", {"form": form, "post": post, "title": title})


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_profile).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {'profile':user_profile,
                                            'page':page,
                                            'paginator':paginator,})

def page_not_found(request, exception): # noqa, pylint: disable=unused-argument
    return render(request, "misc/404.html", {"path": request.path}, status=404)

def server_error(request):
    return render(request, "misc/500.html", status=500)

def add_group(request):
    title = 'Добавить тэг'
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.slug = slugify(group.title)
            form.save()
            return redirect("group", slug=group.slug)
        return render(request, "new_post.html", {'form':form, 'title':title})
    form = GroupForm()
    return render(request, "new_post.html", {'form':form, 'title':title})

def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_view.html', {'post':post})
