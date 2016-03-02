from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Comment, Category, Tag


def hello(request):
    return HttpResponse('hello world')

def hello_with_template(request):
    return render(request, 'hello.html')

def list_posts(request):
    per_page = 5
    current_page = int(request.GET.get('page', 1)) # page가 있으면 값을 가져오고 없으면 1을 가져온다.

    all_posts = Post.objects.select_related().prefetch_related().all()

    pagi = Paginator(all_posts, per_page)
    try:
        pg = pagi.page(current_page)
    except PageNotAnInteger:
        pg = pagi.page(1)
    except EmptyPage:
        pg = []

    return render(request, 'list_posts.html', {
        'posts': pg,
    })

def view_post(request, pk):
    the_post = get_object_or_404(Post, pk=pk)
    the_comment = Comment.objects.filter(post=the_post)

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        new_comment = Comment()
        new_comment.content = request.POST.get('content')
        new_comment.post = the_post
        new_comment.save()
        return redirect('view_post', pk=the_post.pk)

    return render(request, 'view_post.html', {
        'post': the_post,
        'comment' : the_comment,
    })

def create_post(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        new_post = Post()
        new_post.title = request.POST.get('title') # 사용자가 잘못된 입력값을 주는 경우 예외처리를 좀 생각해 보자. 서버에서 검증하는 방법.
        new_post.content = request.POST.get('content')

        category_pk = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_pk)
        new_post.category = category
        new_post.save()
        return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html', {
        'categories': categories,
    })

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        post_edit = request.POST
        post.title = post_edit['title']
        post.content = post_edit['content']

        category = get_object_or_404(Category, pk=post_edit['category'])
        post.category = category
        post.save()
        return redirect('view_post', pk=post.pk)

    return render(request, 'edit_post.html', {
        'post': post,
        'categories': categories,
    })

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        post.delete()
        return redirect('list_posts')

    return render(request, 'delete_post.html', {
        'post': post,
    })

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method =='POST':
        comment.delete()
        return redirect('view_post', pk=comment.post.pk)

    return render(request, 'delete_comment.html',{
        'comment':comment,
    })
