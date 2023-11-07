# imports
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator  # nummering of pages
from django.shortcuts import redirect, render  # HTML things
from django.urls import reverse_lazy  # redirect but better
from django.views.generic import ListView, DetailView, CreateView, FormView  # django classes for rendering web pages
from django.contrib.auth.mixins import LoginRequiredMixin  # class for no login ppl
import time

from .forms import *
from .models import *
from .utils import DataMixin

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# menu of the site
menu = [{'title': 'About us', 'url_name': 'about'},  #
        {'title': 'Sell', 'url_name': 'sell'},  #
        {'title': 'Feedback form', 'url_name': 'feedback'}]  #


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————

# class based views(CBV) - views прописаний класами
# - ListView:
# Клас ListView використовується для створення сторінки, яка відображає список об'єктів моделі.
# Він автоматично створює список об'єктів з бази даних і рендерить їх у шаблоні для відображення користувачу.

# - DetailView:
# Клас DetailView використовується для відображення деталей конкретного об'єкта моделі.
# Він автоматично завантажує об'єкт з бази даних за його ідентифікатором і
# рендерить його у шаблоні для відображення користувачу.

# - CreateView:
# Клас CreateView використовується для створення нового об'єкта моделі.
# Він надає форму для введення даних користувачем, обробляє дані, введені користувачем,
# і створює новий об'єкт моделі в базі даних.

# - DataMixin:
# Клас для спадкування констант, наприклад пагінація та вигляд меню для незареєстрованого користувача.

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Content:
class ProductHome(DataMixin, ListView):
    paginate_by = 7
    model = Product
    template_name = 'content/index.html'
    # object_list - стандартна змінна для всіх елементів бази даних
    # context_object_name - для зміни стандартної змінної для всіх елементів бази даних
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Main Page')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Product.objects.filter(is_sold=False).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Product
    template_name = 'content/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='post')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ProductCategory(DataMixin, ListView):
    paginate_by = 6
    model = Product
    template_name = 'content/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_sold=False).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Category ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# About page:
def about(request):
    cats = Category.objects.all()
    user_menu = menu.copy()
    total = Product.objects.count()

    if not request.user.is_authenticated:
        user_menu.pop(1)
    context = {
        'title': 'Home',
        'menu': user_menu,
        'cats': cats,
        'total': total
    }
    return render(request, 'menu/about.html', context=context)


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Forms
class Sell(LoginRequiredMixin, DataMixin, CreateView):
    form_class = SellForm
    template_name = 'menu/sell.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='sell')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        new_product = form.save()

        category = new_product.cat

        category.product_count = Product.objects.filter(cat=category).count()
        category.save()

        return redirect('home')


class Feedback(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'menu/feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# ——————————————————————————————————————————————————————————————————
# Registration things
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'menu/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'menu/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='login')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


# def show_profile(request):
#     username = User.username
#     context = {
#         'slug_url_kwarg': username
#     }
#
#     return render(request, 'menu/profile.html', context=context)


class ShowProfile(DataMixin, DetailView):
    model = User
    template_name = 'content/profile.html'
    slug_url_kwarg = 'profile_slug'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='profile')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Error handlers
def pageNotFound(request, exception):
    time.sleep(10)
    redirect('content/index.html')
    return render(request, 'errors/404.html')
