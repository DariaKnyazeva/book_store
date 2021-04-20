from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Div, Field, HTML

from django import forms

from books.models import Book


def get_styled_submit_button(name="submit", caption="Submit", icon="fa-check", style="btn-primary"):
    return HTML(f'<button type="submit" name="{name}" class="btn {style}"><i class="fa {icon}"></i> {caption}</button>')


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Title',
                        widget=forms.TextInput(attrs={'type': 'search',
                                                      'class': 'input-large search-query'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Title'
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = "form-search"
        self.helper.layout = Layout(
            Div(
                Div(Field('q'), css_class="col-md-7"),
                css_class='row'
            ),
            ButtonHolder(
                Div(get_styled_submit_button('submit', 'Search',
                                             icon='fa-search',
                                             style='btn-success'),
                    ),
            ),
        )

    def search(self):
        query = self.cleaned_data.get('q', '').strip()
        return Book.objects.filter(title__icontains=query)
