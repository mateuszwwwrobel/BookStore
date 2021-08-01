import requests
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib import messages
from rest_framework import viewsets

from core.forms import AddBookForm
from core.models import Author, Book
from core.serializers import BookSerializer, AuthorSerializer


class HomeView(TemplateView):
    template_name = 'index.html'


class FindBookView(View):
    """Allows users to search for books by given parameters."""
    def get(self, request):
        title = request.GET.get('title')
        author = request.GET.get('author')
        language = request.GET.get('language')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        filter_dict = {}

        if self.is_valid_queryparam(title):
            filter_dict['title'] = title

        if self.is_valid_queryparam(author):
            try:
                author_id = Author.objects.get(name=author)
            except ObjectDoesNotExist:
                messages.info(request, 'Author has not been found.')
            else:
                filter_dict['author'] = author_id

        if self.is_valid_queryparam(language):
            filter_dict['language'] = language

        if self.is_valid_queryparam(from_date):
            filter_dict['pub_date__gte'] = from_date

        if self.is_valid_queryparam(to_date):
            filter_dict['pub_date__lt'] = to_date

        if filter_dict:
            queryset = Book.objects.filter(**filter_dict)
        else:
            messages.info(request, 'Please find list of all books down below.')
            queryset = Book.objects.all()

        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'queryset': queryset,
            'page_obj': page_obj,
        }

        return render(request, 'find_book.html', context)

    @staticmethod
    def is_valid_queryparam(param):
        return param != '' and param is not None


class AddBookView(View):
    """Allows users to add new books to database via the form."""
    def get(self, request):
        authors = Author.objects.all()
        form = AddBookForm(data_list=authors)

        context = {
            'form': form,
        }

        return render(request, 'add_book.html', context)

    def post(self, request):
        authors = Author.objects.all()
        author = Author.objects.get_or_create(name=request.POST['author'])
        request.POST = request.POST.copy()
        request.POST['author'] = str(author[0].id)
        form = AddBookForm(request.POST)

        if len(request.POST['pub_date']) != 10:
            messages.info(request, 'Wrong date format, please try again.')
            context = {
                'form': AddBookForm(request.POST, data_list=authors),
            }
            return render(request, 'add_book.html', context)

        if len(request.POST['isbn']) != 13:
            messages.info(request, 'ISBN number must have 13 digits. Please try again.')
            context = {
                'form': AddBookForm(request.POST, data_list=authors),
            }
            return render(request, 'add_book.html', context)

        if form.is_valid():
            form.save()
            messages.success(request, 'Book successfully added to database!')

        context = {
            'form': AddBookForm(data_list=authors),
        }

        return render(request, 'add_book.html', context)


class ImportBookView(View):
    """Allows users to add books through the Google Books APIs."""
    def get(self, request):
        search_phrase = request.GET.get('search_phrase')

        if search_phrase:
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search_phrase}&fields=items(volumeInfo'
                             '(title,authors,publishedDate,industryIdentifiers,pageCount,imageLinks(thumbnail),language))')

            books_instances = []
            if r.status_code == 200:
                try:
                    books = r.json()['items']
                except KeyError:
                    books = []
                    messages.success(request, 'No books with the searched phrase.')

                for book in books:
                    book_info = book['volumeInfo']
                    title = book_info.get('title')
                    language = book_info.get('language')
                    pages = book_info.get('pageCount') if book_info.get('pageCount') else 0

                    pub_date = book_info.get('publishedDate')
                    try:
                        pub_date_length = len(pub_date)
                    except TypeError:
                        pub_date_length = 0
                    if pub_date_length == 7:
                        pub_date += '-01'
                    elif pub_date_length == 4:
                        pub_date += '-01-01'

                    try:
                        author = Author.objects.get_or_create(name=book_info.get('authors')[0])[0]
                    except TypeError:
                        author = Author.objects.get_or_create(name='Unknown')[0]

                    isbn_codes = book_info.get('industryIdentifiers')
                    if isbn_codes:
                        for code in isbn_codes:
                            if code['type'] == 'ISBN_13':
                                isbn_13 = code['identifier']
                                isbn = isbn_13
                                break
                            if code['type'] == 'ISBN_10':
                                isbn_10 = code['identifier']
                                isbn = isbn_10
                                continue
                            if code['type'] == 'OTHER':
                                isbn_other = code['identifier']
                                if 'isbn' not in locals():
                                    isbn = isbn_other
                    else:
                        continue

                    try:
                        cover_urls = book_info.get('imageLinks')['thumbnail']
                    except TypeError:
                        cover_urls = 'http://www.hallens.co.uk/wp-content/themes/consultix/images/no-image-found-360x260.png'

                    try:
                        new_book = Book.objects.create(
                            title=title,
                            author=author,
                            pub_date=pub_date,
                            isbn=isbn,
                            pages=pages,
                            cover_url=cover_urls,
                            language=language,
                        )
                    except IntegrityError:
                        continue
                    except ValidationError:
                        continue

                    books_instances.append(new_book)

                if books_instances:
                    messages.success(request, 'Books have been added to database.')
                else:
                    messages.success(request, 'No new books have been added to database.')

            context = {
                'books': books_instances,
            }

            return render(request, 'api_book.html', context)
        else:
            return render(request, 'api_book.html')


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
