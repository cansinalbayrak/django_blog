from django.shortcuts import render, get_object_or_404,HttpResponseRedirect, redirect
from .models import Post, Category, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def index(request):
    context = dict()
    posts_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = posts_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__first_name__icontains=query)
        ).distinct()

    paginator = Paginator(posts_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context['post'] = posts
    context['posts_list'] = Post.objects.all()
    context['cat'] = Category.objects.all()
    context['popular_list'] = Post.objects.all().order_by('-read', '-id')[:3]
    return render(request, 'index.html', context)
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    read = post.read
    read += 1
    degis = Post.objects.filter(slug=slug).update(read=read)

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'detail.html', context)

def add_comment_to_post(request, pk):
    post = Post.get_object_or_404(Post, pk=pk)

    if request.POST == "POST":
        form  = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'forms.html', {'form': form})


@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('detail', pk = comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('detail', pk = comment.post.pk)


def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category, slug=category_slug,
    )

    context['items'] = Post.objects.filter(
        category=context['category'],
    )

    return render(request, 'category_show.html', context)
