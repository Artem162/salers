from django.db.models import Count

from .models import *

menu = [{'title': 'About us', 'url_name': 'about'},  #
        {'title': 'Sell', 'url_name': 'sell'},  #
        {'title': 'Feedback form', 'url_name': 'feedback'}]  #


class DataMixin:
    paginated_by = 8

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        if not cats:
            cats = Category.objects.annotate(Count('product'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
