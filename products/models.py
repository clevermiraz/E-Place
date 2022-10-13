from django.db import models
import uuid
from django.urls import reverse
from account.models import Profile
from PIL import Image
from django.utils.text import slugify
from tinymce.models import HTMLField


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book_image = models.ImageField(
        default='default_book.png', null=True, blank=True, upload_to='books_images')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('books:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        img = Image.open(self.book_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.book_image.path)
