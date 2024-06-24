# -*- coding: utf-8 -*-

from haystack.views import SearchView as BaseSearchView
from djconfig import config

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..comment.models import Comment
from .forms import AdvancedSearchForm
from ..core.utils.paginator import yt_paginate


class SearchView(BaseSearchView):
    """
    This view does not pre load data from\
    the database (``load_all=False``),\
    all required fields to display the\
    results must be stored (ie: ``indexed=False``).

    Avoid doing ``{{ result.object }}`` to\
    prevent database hits.
    """
    def __init__(self, *args, **kwargs):  # no-qa
        super(SearchView, self).__init__(
            template='spirit/search/search.html',
            form_class=AdvancedSearchForm,
            load_all=False)

    def __call__(self, request):
        return super(SearchView, self).__call__(request)

    def build_page(self):
        s1 = self.request.GET.get('q')
        if not s1:
            return None, []
        s1 = s1.lower()
        comments = [
            (x, y) for x in self.results
            for y in Comment.objects.filter(topic_id=x.pk)
            if y.comment.lower().find(s1) >= 0 and not y.is_removed
        ]
        paginator = None
        page0 = yt_paginate(
            comments,
            per_page=config.topics_per_page,
            page_number=self.request.GET.get('page', 1))
        # breakpoint()
        page = []
        for r in page0:
            d0 = dict(r[0].get_stored_fields(), title=r[1].comment)
            c_id = r[1].id
            n_page = 1 + c_id // 20
            if n_page > 1:
                d0['slug'] += f'/?page={n_page}'
            d0['slug'] += f'#c{c_id}'
            page.append({'fields': d0, 'pk': r[0].pk})
        return paginator, page
