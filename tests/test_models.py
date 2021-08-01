from django.test import TestCase
from core.models import Author, Book


class AuthorModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(name="Tolkien")

    # Author Model
    def test_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_author_created_at_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_author_updated_at_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    def test_author_name_max_length(self) -> None:
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('name').max_length
        self.assertEqual(max_length, 256)

    def test_string_representation_author(self) -> None:
        author = Author.objects.get(id=1)
        expected_obj_name = f'{author.name}'
        self.assertEqual(str(author), expected_obj_name)


class BookModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        author = Author.objects.create(name="Tolkien")
        Book.objects.create(
            title='Hobbit',
            author=author,
            pub_date='2020-06-06',
            isbn=1234567890000,
            pages=133,
            cover_url='http://ladny_url.com/okladka/',
            language='pl',
        )

    # Book  Model
    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'isbn')

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_pub_date_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'pub date')

    def test_pages_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('pages').verbose_name
        self.assertEqual(field_label, 'pages')

    def test_cover_url_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('cover_url').verbose_name
        self.assertEqual(field_label, 'cover url')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_created_at_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    def test_title_max_length(self) -> None:
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 256)

    def test_isbn_max_length(self) -> None:
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_language_max_length(self) -> None:
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('language').max_length
        self.assertEqual(max_length, 10)

    def test_string_representation_book(self) -> None:
        book = Book.objects.get(id=1)
        expected_obj_name = f'{book.title} - {book.author}'
        self.assertEqual(str(book), expected_obj_name)
