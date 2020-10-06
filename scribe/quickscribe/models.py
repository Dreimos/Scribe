import datetime
from django.conf import settings
from django.urls import reverse
from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField

YEAR_CHOICES = [(r,r) for r in reversed(range(1900, datetime.datetime.now().year+1))]

def default_year():
    return datetime.datetime.now().year

class Selectors(models.Model):
    name = models.CharField("Name", max_length=50)
    slug = AutoSlugField("Adress", unique=True, always_update=False, populate_from="name")
    description = models.TextField("Description", blank=True, default="No description")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Genre(Selectors):
    pass

class Tag(Selectors):
    pass

class Language(Selectors):
    pass

class Novel(models.Model):
    name = models.TextField("Name", unique=True, max_length=500)
    alt_name = models.TextField("Alternative title(s)", blank=True, max_length=1000)
    slug = AutoSlugField("Slug", unique=True, always_update=False, populate_from="name")
    author = models.CharField("Author(s)", max_length=255)
    artist = models.CharField("Artist(s)", blank=True, max_length=255)
    year = models.IntegerField("Year of publication", choices=YEAR_CHOICES, default=default_year)
    publisher = models.CharField("Publisher", blank=True, max_length=255)
    licensed = models.BooleanField("Licensed", default=False)
    coo_status = models.TextField("Status in COO", blank=True)
    fully_translated = models.BooleanField("Fully Translated", default=False)
    genres = models.ManyToManyField("Genre", verbose_name="Genres")
    tags = models.ManyToManyField("Tag", verbose_name="Tags")
    language = models.ForeignKey("Language", verbose_name="Language", on_delete=models.CASCADE)
    description = models.TextField("Description", blank=True, max_length=5000)
    cover = models.ImageField("Cover", blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quickscribe:novel-detail", kwargs={"slug": self.slug})

class Chapter(models.Model):
    name = models.CharField("Title", max_length=255)
    content = RichTextField("Chapter content")
    novel = models.ForeignKey("Novel", on_delete=models.CASCADE)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    uploaded = models.DateTimeField("Upload date", auto_now_add=True)
    updated = models.DateTimeField("Last update", blank=True, default=datetime.datetime.now())
    views = models.IntegerField("Chapter views", default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quickscribe:chapter-detail", kwargs={"pk": self.id})
