# from django_filters.views import FilterView
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse

from books.models import Book, BookRent
from pricing.models import Currency, Price
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
        params = params.split('&')
        if params and params[0].startswith('page'):
            params.pop(0)
        params = '&'.join(params)
        context['params'] = params
        return context


class SearchViewMixin(PaginationMixin):
    searchqueryset = None

    def build_form(self):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = self.get_initial()
        kwargs = {}
        kwargs.update(self.get_form_kwargs())

        return self.form_class(data=data, **kwargs)

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

    def get_initial(self):
        return {
            'q': self.request.GET.get('q', ''),
        }

    def get_pagination_url(self):
        return reverse('books:book-list')

    # def dispatch(self, *args, **kwargs):
    #     import ipdb; ipdb.set_trace()
    #     return super().dispatch(*args, **kwargs)


class BookRentView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return

        book_id = request.POST.get('book')
        book = get_object_or_404(Book, id=book_id)
        # books = request.POST.getlist('book[]')

        currency = Currency.get_default_currency()
        price, _ = Price.objects.get_or_create(amount=1, currency=currency)
        BookRent.objects.create(customer=request.user, book=book,
                                price=price, status=BookRent.Status.RENTED)
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
