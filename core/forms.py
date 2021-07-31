from django import forms
from core.models import Book


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'
        result = text_html + data_list
        return result


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'pub_date': 'Date of Publication',
            'isbn': 'ISBN Number',
            'cover_url': 'Link to the cover',
        }

    def __init__(self, *args, **kwargs):
        _authors_list = kwargs.pop('data_list', None)
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = ListTextWidget(data_list=_authors_list, name='authors_list')
