from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import Book
from store.serializers import BooksSerializer

from store.models import UserBookRelation



class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Erich', last_name='Remark')
        user2 = User.objects.create(username='user2', first_name='Emil', last_name='Zolia')
        user3 = User.objects.create(username='user3', first_name='Franc', last_name='Kafka')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=50, author_name='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                #'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67',
                'readers': [
                    {
                        'first_name': 'Erich',
                        'last_name': 'Remark'
                    },

                    {
                        'first_name': 'Emil',
                        'last_name': 'Zolia'
                    },

                    {
                        'first_name': 'Franc',
                        'last_name': 'Kafka'
                    }
                ]

            },
            
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '50.00',
                'author_name': 'Author 2',
                #'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50',
                'readers': [
                    {
                        'first_name': 'Erich',
                        'last_name': 'Remark'
                    },

                    {
                        'first_name': 'Emil',
                        'last_name': 'Zolia'
                    },

                    {
                        'first_name': 'Franc',
                        'last_name': 'Kafka'
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, data)
