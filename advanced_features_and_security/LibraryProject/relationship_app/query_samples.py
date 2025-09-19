import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from .models import Author, Book, Library, Librarian

# --- Query 1: Query all books by a specific author ---
def get_books_by_author(author_name):
 
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author) 
        print(f"\n--- Books by {author.name} ---")
        if not books:
            print("No books found for this author.")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"\nAuthor '{author_name}' not found.")

# --- Query 2: List all books in a library ---
def get_all_books_in_library(library_name):

    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\n--- All books in {library.name} Library ---")
        if not books:
            print("No books found in this library.")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"\nLibrary '{library_name}' not found.")

# --- Query 3: Retrieve the librarian for a library ---

def get_librarian_for_library(library_name):
    """
    Retrieves and prints the librarian for a specific library.
    """
    try:
        # Find the librarian whose library field matches the given library name
        librarian = Librarian.objects.get(library=library_name)
        
        print(f"\n--- Librarian for {librarian.library.name} Library ---")
        print(f"Name: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"\nLibrary '{library_name}' has no assigned librarian.")


if __name__ == "__main__":
 
    pass