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