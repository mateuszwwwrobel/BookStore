from random import randint, randrange
from datetime import timedelta, datetime

from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from core.models import Author, Book
from core.forms import AddBookForm
from core.views import FindBookView


def random_with_n_digits(n):
    """Creates a random number with the given digit length."""
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class FindBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 18
        author = Author.objects.create(name="Tolkien")

        dt1 = datetime.strptime('1/1/2000', '%m/%d/%Y')
        dt2 = datetime.strptime('1/1/2010', '%m/%d/%Y')

        for author_id in range(number_of_authors):
            Book.objects.create(
                title=f'Book {author_id}',
                author=author,
                pub_date=random_date(dt1, dt2),
                isbn=random_with_n_digits(13),
                pages=133,
                cover_url='http://cover_url.pl/',
                language='pl',
            )

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/find-book')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('find-book'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('find-book'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_lists_all_books(self):
        # Get second page and confirm it has (exactly) remaining 8 items
        response = self.client.get(reverse('find-book') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 8)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('find-book') + '?title=Book 2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'find_book.html')

    def test_filter_books_by_title(self):
        response = self.client.get(reverse('find-book') + '?title=Book 2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_filter_books_by_author_and_title(self):
        response = self.client.get(reverse('find-book') + '?title=Book 2&author=Tolkien')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_filter_books_by_author_and_title_and_language(self):
        response = self.client.get(reverse('find-book') + '?title=Book 2&author=Tolkien&language=pl')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_filter_books_by_dates_range(self):
        response = self.client.get(reverse('find-book') + '?from_date=2005-01-01&to_date=2009-01-01')

        qs = Book.objects.filter(pub_date__gte=datetime.fromisoformat("2005-01-01")). \
            filter(pub_date__lt=datetime.fromisoformat("2009-01-01"))
        qs_length = 10 if len(qs) > 10 else len(qs)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), qs_length)

    def test_message_info(self):
        response = self.client.get(reverse('find-book'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please find list of all books down below.')

    def test_message_info_when_author_not_found(self):
        response = self.client.get(reverse('find-book') + '?author=Sapkowski')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), 'Author has not been found.')
        self.assertEqual(str(messages[1]), 'Please find list of all books down below.')

    def test_function_is_valid_queryparam(self) -> None:
        self.assertEqual(FindBookView.is_valid_queryparam(''), False)
        self.assertEqual(FindBookView.is_valid_queryparam(None), False)
        self.assertEqual(FindBookView.is_valid_queryparam('param_value'), True)


class HomeViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class AddBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        author = Author.objects.create(name="Tolkien")

        dt1 = datetime.strptime('1/1/2000', '%m/%d/%Y')
        dt2 = datetime.strptime('1/1/2010', '%m/%d/%Y')

        for author_id in range(number_of_authors):
            Book.objects.create(
                title=f'Book {author_id}',
                author=author,
                pub_date=random_date(dt1, dt2),
                isbn=random_with_n_digits(13),
                pages=133,
                cover_url='http://cover_url.pl/',
                language='pl',
            )

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/add-book')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('add-book'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('add-book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_context_has_all_data(self) -> None:
        response = self.client.get(reverse('add-book'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddBookForm)

    def test_create_new_book_successfully(self) -> None:
        author = Author.objects.get(id=1)
        books_length = len(Book.objects.all())
        response = self.client.post(reverse('add-book'),
                                    {'author': author,
                                     'pub_date': '2021-01-01',
                                     'isbn': 1212121212121,
                                     'language': 'pl',
                                     'title': 'The Witcher',
                                     'pages': 234,
                                     'cover_url': 'http://cover.pl/',
                                     })
        self.assertEqual(len(Book.objects.all()), books_length + 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Book successfully added to database!')

    def test_create_new_book_when_pub_date_incorrect(self) -> None:
        author = Author.objects.get(id=1)
        response = self.client.post(reverse('add-book'),
                                    {'author': author,
                                     'pub_date': '2021-01',
                                     'isbn': 1212121212121,
                                     'language': 'pl',
                                     'title': 'The Witcher',
                                     'pages': 234,
                                     'cover_url': 'http://cover.pl/',
                                     })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wrong date format, please try again.')

    def test_create_new_book_when_isbn_incorrect(self) -> None:
        author = Author.objects.get(id=1)
        response = self.client.post(reverse('add-book'),
                                    {'author': author,
                                     'pub_date': '2021-01-01',
                                     'isbn': 1212121,
                                     'language': 'pl',
                                     'title': 'The Witcher',
                                     'pages': 234,
                                     'cover_url': 'http://cover.pl/',
                                     })

        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'ISBN number must have 13 digits. Please try again.')


class ImportBookViewTest(TransactionTestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        author = Author.objects.create(name="Tolkien")

        dt1 = datetime.strptime('1/1/2000', '%m/%d/%Y')
        dt2 = datetime.strptime('1/1/2010', '%m/%d/%Y')

        for author_id in range(number_of_authors):
            Book.objects.create(
                title=f'Book {author_id}',
                author=author,
                pub_date=random_date(dt1, dt2),
                isbn=random_with_n_digits(13),
                pages=133,
                cover_url='http://cover_url.pl/',
                language='pl',
            )

    def setUp(self) -> None:
        self.client.get(reverse('import-book'), {'search_phrase': 'python'})

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/import-book')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('import-book'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self) -> None:
        response = self.client.get(reverse('import-book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api_book.html')

    def test_when_author_unknown(self) -> None:
        self.client.get(reverse('import-book'), {'search_phrase': 'gruba'})
        self.assertRaises(TypeError)

    def test_when_incomplete_pub_date(self) -> None:
        self.client.get(reverse('import-book'), {'search_phrase': 'niemcy'})
        self.assertRaises(TypeError)

    def test_when_cover_not_found(self) -> None:
        self.client.get(reverse('import-book'), {'search_phrase': 'zamek'})
        self.assertRaises(TypeError)

    def test_when_import_books_successfully(self) -> None:
        response = self.client.get(reverse('import-book'), {'search_phrase': 'woda'})

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Books have been added to database.')

    def test_when_no_books_found(self) -> None:
        response = self.client.get(reverse('import-book'), {'search_phrase': 'python543t43gdfgdf53453453'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 2)
        self.assertRaises(KeyError)
        self.assertEqual(str(messages[0]), 'No books with the searched phrase.')
        self.assertEqual(str(messages[1]), 'No new books have been added to database.')

    def test_when_books_in_db_already(self) -> None:
        response = self.client.get(reverse('import-book'), {'search_phrase': 'python'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'No new books have been added to database.')
