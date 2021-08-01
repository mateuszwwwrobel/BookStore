from django.test import TestCase
from core.forms import AddBookForm, ListTextWidget


class FormsTestCase(TestCase):

    def test_add_book_form_custom_labels(self) -> None:
        form = AddBookForm()
        self.assertTrue(form.fields['isbn'].label is None or form.fields['isbn'].label == 'ISBN Number')
        self.assertTrue(form.fields['pub_date'].label is None or form.fields['pub_date'].label == 'Date of Publication')
        self.assertTrue(form.fields['cover_url'].label is None or form.fields['cover_url'].label == 'Link to the cover')

    def test_add_book_form_widget(self) -> None:
        form = AddBookForm()
        self.assertIsInstance(form.fields['author'].widget, ListTextWidget)
