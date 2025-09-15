retrieved_book = Book.objects.get(title="1984")
print(f"Retrieved Title: {retrieved_book.title}")
print(f"Retrieved Author: {retrieved_book.author}")
print(f"Retrieved Year: {retrieved_book.publication_year}")