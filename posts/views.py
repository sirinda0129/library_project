from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm
import datetime as dt
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required


User = get_user_model()

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    # функция get_object_or_404 позволяет получить объект из базы данных 
    # по заданным критериям или вернуть сообщение об ошибке если объект не найден
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    count = posts.count
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "posts": posts, 'page': page, 'paginator': paginator, 'count' : count})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files =request.FILES or None)
        if form.is_valid():
            Post.objects.create(
                author = request.user,
                text = form.cleaned_data['text'],
                url = form.cleaned_data['url'],
                group = form.cleaned_data['group'],
                )
            return redirect("index")
    form = PostForm()
    return render(request, "new_post.html", {"form": form})

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("index")
    # добавим в form свойство files
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, "post_edit.html", {"form": form, "post": post},)


def profile(request, username):
    author = get_object_or_404(User, username = username)
    posts = Post.objects.filter(author = author).order_by('-pub_date')
    count = posts.count
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # тут тело функции
    return render(request, "profile.html", {
        'author':author,
        'posts' : posts,
        'page': page,
        'paginator': paginator,
        'count' : count,
        } )

def page_not_found(request, exception):
        # Переменная exception содержит отладочную информацию, 
        # выводить её в шаблон пользователской страницы 404 мы не станем
        return render(request, "misc/404.html", {"path": request.path}, status=404)

def server_error(request):
        return render(request, "misc/500.html", status=500)