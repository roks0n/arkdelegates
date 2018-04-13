from django.http import HttpResponse
from django.views.generic.base import TemplateView
from app.models import Delegate
from app.utils import is_staff
from app.sql import sql_delegates
from django.core.paginator import Paginator


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


class Homepage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        delegates = Delegate.objects.raw(sql_delegates)
        delegates_list = list(delegates)

        page = int(self.request.GET.get('page', 1))
        paginator = Paginator(list(delegates_list), 60)
        delegates_paginated = paginator.get_page(page)

        if self.request.user.is_authenticated:
            logged_in_delegate = self.request.user.delegate
        else:
            logged_in_delegate = None

        context.update({
            'seo': {
                'title': 'ARK Delegates - Find and follow ARK delegates',
                'description': (
                    'Find ARK delegates that you want to support and follow their progress.'
                )
            },
            'delegates': delegates_paginated,
            'is_staff': is_staff(self.request.user),
            'paginator': delegates_paginated,
            'logged_in_delegate': logged_in_delegate
        })

        return context
