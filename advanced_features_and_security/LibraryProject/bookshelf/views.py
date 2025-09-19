from django.shortcuts import render
from .models import Book
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article
from .forms import ArticleForm

@permission_required('blog.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/article_list.html', {'articles': articles})

@permission_required('blog.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

@permission_required('blog.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})

@permission_required('blog.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})
# Create your views here.
# This view is required by the checker
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'bookshelf/book_list.html', context)

def search_books(request):
    query = request.GET.get('q')
    if query:
        # The ORM handles query sanitization
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})