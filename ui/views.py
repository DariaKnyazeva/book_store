# from django_filters.views import FilterView
from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('books:book-list')

        return super().dispatch(request, *args, **kwargs)


class CoverageView(TemplateView):
    template_name = 'coverage/index.html'
