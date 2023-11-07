from django.db import models
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Description')  # content
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None, verbose_name='Price')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Photo')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Latest update time')
    is_sold = models.BooleanField(default=False, verbose_name='Out of stock?')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Category')

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Goods'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    product_count = models.IntegerField(default=0, verbose_name='Product Count')

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
        ordering = ['id']
