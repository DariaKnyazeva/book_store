# from django_filters.views import FilterView
import logging


from django.shortcuts import redirect
from django.views.generic.base import TemplateView


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        logger.debug("Index view called")

        if request.user.is_authenticated:
            return redirect('books:book-list')

        return super().dispatch(request, *args, **kwargs)


class CoverageView(TemplateView):
    template_name = 'coverage/index.html'
