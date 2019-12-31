from django.db import models
from datetime import date
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Concert(models.Model):
    artist = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.artist} {self.location}'

    # def get_absolute_url(self):
    #     return ('')

class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"
