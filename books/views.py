# from django_filters.views import FilterView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse

from books.models import Book, BookRent
from .recipe import Recipe
from .forms import BookSearchForm


class PaginationMixin:
    paginate_by = settings.PAGINATED_BY

    def get_pagination_url(self):
        raise NotImplementedError()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagination_url'] = self.get_pagination_url()
        params = self.request.META.get('QUERY_STRING', '')
        first, *rest = params.split("&", maxsplit=1)
        if first.startswith("page"):
            params = rest[0] if rest else []
        context['params'] = params
        return context


class SearchViewMixin(PaginationMixin):
    searchqueryset = None

    def build_form(self):
        """
        Instantiates the form the class should use to process the search query.
        """
        return self.form_class(data=self.get_initial(),
                               **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.build_form()
        context['search_form'] = form
        # context['suggestion'] = form.get_suggestion()
        return context

    def get_queryset(self):
        form = self.build_form()
        if form.is_valid():
            return form.search()
        return self.searchqueryset

    def get_initial(self):
        return {
            'q': self.request.GET.get('q', ''),
        }

    def get_form_kwargs(self):
        return {
            # 'customer': self.request.user
        }


class BookListView(SearchViewMixin, ListView):
    model = Book
    template_name = 'book_store/book_list.html'
    form_class = BookSearchForm

    def get_pagination_url(self):
        return reverse('books:book-list')


class BookRentView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return

        book_id = request.POST.get('book')
        book = get_object_or_404(Book, id=book_id)
        # books = request.POST.getlist('book[]')

        BookRent.objects.create(customer=request.user, book=book,
                                status=BookRent.Status.RENTED)
        return HttpResponse('OK')


class ReceitView(TemplateView):
    template_name = 'book_store/receit.html'
    form_class = BookSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rented_books'] = self.recipe.rents
        context['price'] = self.recipe.get_price()
        return context

    def dispatch(self, *args, **kwargs):
        self.recipe = Recipe(self.request.user)
        return super().dispatch(*args, **kwargs)
