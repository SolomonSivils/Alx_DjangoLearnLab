from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm  # We'll define this in Step 2
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden # To handle unauthorized access

# ... (Existing imports for Post CRUD views and Post model) ...
from .models import Comment  # Import the new Comment model
from .forms import CommentForm # Import the new CommentForm
# Note: We keep the old views for context, but the new CBVs handle post logic

# -----------------------------------------------------------------
# READ: List all posts (Accessible to all users)
# -----------------------------------------------------------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_list.html
    context_object_name = 'posts'         # Renames object_list to posts
    ordering = ['-published_date']        # Orders posts by newest first

# -----------------------------------------------------------------
# READ: View a single post (Accessible to all users)
# -----------------------------------------------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # blog/post_detail.html

# -----------------------------------------------------------------
# CREATE: Create a new post (Requires login)
# -----------------------------------------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # Use the form we define in Step 2
    form_class = PostForm 
    template_name = 'blog/post_form.html'
    
    # Override form_valid to automatically set the author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# -----------------------------------------------------------------
# UPDATE: Edit an existing post (Requires login AND author check)
# -----------------------------------------------------------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Automatically set the author (optional, but good practice)
        form.instance.author = self.request.user
        return super().form_valid(form)

    # test_func is required by UserPassesTestMixin to check permissions
    def test_func(self):
        post = self.get_object()
        # Returns True only if the logged-in user is the post's author
        return self.request.user == post.author 

# -----------------------------------------------------------------
# DELETE: Delete a post (Requires login AND author check)
# -----------------------------------------------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    # Use reverse_lazy to redirect to the post list after deletion
    success_url = reverse_lazy('post-list') 

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# ... (Post CRUD views here) ...

# -----------------------------------------------------------------
# POST DETAIL VIEW MODIFICATION (Implicit: We need to pass the form)
# -----------------------------------------------------------------
# We don't need to change PostDetailView, as we will use the related 
# name 'comments' in the template to display existing comments.

# -----------------------------------------------------------------
# CREATE: Add Comment (Requires login)
# -----------------------------------------------------------------
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            
            # Set the foreign keys before saving
            comment.post = post
            comment.author = request.user
            
            comment.save()
            messages.success(request, "Your comment has been posted!")
            
            # Redirect back to the post detail page
            return redirect('post-detail', pk=post.pk)
        else:
             messages.error(request, "Comment could not be posted. Please check the content.")
    
    # If the request method is GET, just redirect back (shouldn't happen often)
    return redirect('post-detail', pk=post.pk)


# -----------------------------------------------------------------
# DELETE: Delete Comment (Requires login AND author check)
# -----------------------------------------------------------------
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Permission Check: Ensure only the author can delete the comment
    if request.user != comment.author:
        return HttpResponseForbidden("You do not have permission to delete this comment.")

    post_pk = comment.post.pk # Save the post ID before deletion
    
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post-detail', pk=post_pk)
    
    # If a GET request somehow lands here, redirect to post detail 
    return redirect('post-detail', pk=post_pk)

3.2 Update blog/urls.py (Adding Comment URLs)
Add the new URL patterns for creating and deleting comments.

File: blog/urls.py (Update)

Python

# blog/urls.py

# ... (Existing imports and Post CRUD paths) ...

urlpatterns = [
    # ... (Post CRUD paths: '', 'post/<int:pk>/', 'post/new/', etc.) ...
    
    # Comment paths
    path('post/<int:pk>/comment/new/', views.add_comment_to_post, name='add-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    
    # ... (Existing auth paths: 'register/', 'profile/') ...
]

# ... (other CBVs) ...

# -----------------------------------------------------------------
# READ: View a single post (Updated to include CommentForm)
# -----------------------------------------------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    # Override get_context_data to add the CommentForm to the template context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass an instance of the CommentForm to the template
        context['form'] = CommentForm() 
        return context
    
# blog/views.py (Add to existing CBV imports)
from django.views.generic import (
    # ... existing imports
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect # Needed for get_success_url

from .models import Post, Comment # Import Comment model
from .forms import PostForm, CommentForm # Import CommentForm

# ... (Existing PostListView, PostDetailView, etc. remain unchanged) ...

# -----------------------------------------------------------------
# CREATE: CommentCreateView (Requires login)
# -----------------------------------------------------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # We don't need a specific template for this, as it will be handled by post_detail.html
    # We set this to None or skip template_name entirely.
    
    # Override form_valid to link the comment to the user and the post
    def form_valid(self, form):
        # 1. Get the Post object from the URL (pk is passed as post_pk)
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        
        # 2. Set the Foreign Keys
        form.instance.post = post
        form.instance.author = self.request.user
        
        # 3. Save the comment and redirect
        return super().form_valid(form)

    # Required to redirect to the post detail page after successful comment creation
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs.get('post_pk')})

# -----------------------------------------------------------------
# UPDATE: CommentUpdateView (Requires login AND author check)
# NOTE: This will require a new template (comment_form.html)
# -----------------------------------------------------------------
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        # Only the author can update the comment
        comment = self.get_object()
        return self.request.user == comment.author

    # Required to redirect to the post detail page after successful update
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

# -----------------------------------------------------------------
# DELETE: CommentDeleteView (Requires login AND author check)
# -----------------------------------------------------------------
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        # Only the author can delete the comment
        comment = self.get_object()
        return self.request.user == comment.author

    # Required to redirect to the post detail page after successful deletion
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    

# blog/views.py

from django.views.generic import (
    ListView,
    # ... other CBV imports ...
)
from django.db.models import Q # Import Q object for search (Crucial for this task!)

# ... (Existing Post/Comment imports) ...

# ... (Existing PostListView, PostDetailView, etc. remain unchanged) ...

# -----------------------------------------------------------------
# READ: View Posts by Tag (New Feature)
# -----------------------------------------------------------------
class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

    def get_queryset(self):
        # Filter posts where the tags contain the tag_slug provided in the URL
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the tag name to the context for the template header
        context['tag_name'] = self.kwargs.get('tag_slug').replace('-', ' ').title()
        return context

# -----------------------------------------------------------------
# READ: Search Posts (New Feature)
# -----------------------------------------------------------------
class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        query = self.request.GET.get('q') # Get the search query from the URL parameter 'q'
        
        if query:
            # Use Q objects to perform a complex OR search across multiple fields
            return Post.objects.filter(
                Q(title__icontains=query) | # Match if title contains query (case-insensitive)
                Q(content__icontains=query) | # Match if content contains query (case-insensitive)
                Q(tags__name__icontains=query) # Match if any tag name contains query
            ).distinct().order_by('-published_date') # distinct() prevents duplicates from the tag match
        
        # If no query is provided, return an empty set
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the original query back to the template
        context['query'] = self.request.GET.get('q')
        return context

# ... (Existing CommentCreateView, etc. remain unchanged) ...