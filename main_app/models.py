from django.db import models
from datetime import date
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

RATINGS = (
  ('1', 'Do Not Watch Again'),
  ('2', 'Did Not Like It'),
  ('3', 'It Was Kinda Good'),
  ('4', 'I Liked It'),
  ('5', 'I Loved This Concert')
)


class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    # concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews_detail', kwargs={'pk': self.id})

class Concert(models.Model):
    artist = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    reviews = models.ManyToManyField(Review)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.artist} {self.location}'

    def get_absolute_url(self):
        return reverse('index')

class Photo(models.Model):
    url = models.CharField(max_length=200)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

