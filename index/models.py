from django.db import models
from datetime import datetime
from django.utils.text import slugify

class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(
        TutorialCategory,
        verbose_name="Category",
        on_delete=models.SET_NULL,  # Change to SET_NULL
        null=True,  # Allow null values
    )
    series_summary = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField("date published", default=datetime.now())

    tutorial_series = models.ForeignKey(
        TutorialSeries,
        verbose_name="Series",
        on_delete=models.SET_NULL,  # Change to SET_NULL
        null=True,  # Allow null values
    )
    tutorial_slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.tutorial_slug:
            self.tutorial_slug = slugify(self.tutorial_title)
        super(Tutorial, self).save(*args, **kwargs)

    def __str__(self):
        return self.tutorial_title
