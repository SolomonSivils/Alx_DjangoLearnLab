retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")
retrieved_book.delete()
all_books = Book.objects.all()
