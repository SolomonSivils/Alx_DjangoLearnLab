from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Author, Book

class BookAPITests(APITestCase):
    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='J.R.R. Tolkien')
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author
        )
        self.list_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.id})
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.id})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.id})

    # Test permissions for unauthenticated users
    def test_unauthenticated_user_cannot_create_book(self):
        """
        Ensure an unauthenticated user cannot create a book.
        """
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_unauthenticated_user_can_list_books(self):
        """
        Ensure an unauthenticated user can list books.
        """
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_unauthenticated_user_can_retrieve_book(self):
        """
        Ensure an unauthenticated user can retrieve a book.
        """
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        
    # Test authenticated user permissions
    def test_authenticated_user_can_create_book(self):
        """
        Ensure an authenticated user can create a book.
        """
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'The Silmarillion', 'publication_year': 1977, 'author': self.author.id}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='The Silmarillion').publication_year, 1977)

    def test_authenticated_user_can_update_book(self):
        """
        Ensure an authenticated user can update a book.
        """
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'The Hobbit (Revised)', 'publication_year': 1937, 'author': self.author.id}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit (Revised)')

    def test_authenticated_user_can_delete_book(self):
        """
        Ensure an authenticated user can delete a book.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # Test filtering functionality
    def test_filtering_by_title(self):
        """
        Ensure filtering by title works correctly.
        """
        response = self.client.get(self.list_url, {'title': self.book1.title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)

    def test_filtering_by_publication_year(self):
        """
        Ensure filtering by publication year works correctly.
        """
        response = self.client.get(self.list_url, {'publication_year': self.book2.publication_year}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book2.title)

    # Test searching functionality
    def test_searching_by_title(self):
        """
        Ensure searching by title works correctly.
        """
        response = self.client.get(self.list_url, {'search': 'Hobbit'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)

    def test_searching_by_author_name(self):
        """
        Ensure searching by author name works correctly.
        """
        response = self.client.get(self.list_url, {'search': 'Tolkien'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    # Test ordering functionality
    def test_ordering_by_title_ascending(self):
        """
        Ensure ordering by title in ascending order works correctly.
        """
        response = self.client.get(self.list_url, {'ordering': 'title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')
        self.assertEqual(response.data[1]['title'], 'The Lord of the Rings')

    def test_ordering_by_publication_year_descending(self):
        """
        Ensure ordering by publication year in descending order works correctly.
        """
        response = self.client.get(self.list_url, {'ordering': '-publication_year'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], self.book2.publication_year)
        self.assertEqual(response.data[1]['publication_year'], self.book1.publication_year)
