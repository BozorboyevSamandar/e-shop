from django.db import models
from django.utils.text import slugify

from basic.utils import get_random_code


class Category(models.Model):
    STATUS = [
        ('Have', 'Have'),
        ('No Have', 'No Have'),
    ]
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_image/', blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    __initial_title = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_title = self.title

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.title != self.__initial_title or self.slug == "":
            if self.title:
                to_slug = slugify(str(self.title))
                ex = Category.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Category.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.title)
        self.slug = to_slug
        super().save(*args, **kwargs)


class Product(models.Model):
    STATUS = [
        ('Have', 'Have'),
        ('No Have', 'No Have'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product_image/', blank=False, null=False)
    count = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_title = self.title

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.title != self.__initial_title or self.slug == "":
            if self.title:
                to_slug = slugify(str(self.title))
                ex = Category.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Category.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.title)
        self.slug = to_slug
        super().save(*args, **kwargs)

class Advertising(models.Model):
    img = models.ImageField(upload_to='advertising_img/', blank=False, null=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
