from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #this is a class and therefore using upper camel casing
import uuid
import boto3
from .models import Concert, Review, Photo
from .forms import ReviewForm

class ConcertCreate(LoginRequiredMixin, CreateView):
  model = Concert
  fields = ['artist', 'location', 'date', 'time']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user #form.instance is the concert
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class ConcertUpdate(LoginRequiredMixin, UpdateView):
  model = Concert
  fields = ['artist', 'location', 'date', 'time']

class ConcertDelete(LoginRequiredMixin, DeleteView):
  model = Concert
  success_url = '/concerts/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def concerts_index(request):
  concerts = Concert.objects.filter(user=request.user)
  return render(request, 'concerts/index.html', { 'concerts' : concerts })

@login_required
def concerts_detail(request, concert_id):
  concert = Concert.objects.get(id=concert_id)
  reviews_concert_doesnt_have = Review.objects.exclude(id__in = concert.reviews.all().values_list('id'))
  reviews_form = ReviewForm()
  return render(request, 'concerts/detail.html', { 
    'concert' : concert,
    'reviews_form': reviews_form,
    'reviews': reviews_concert_doesnt_have
    })

@login_required
def add_review(request, concert_id):
  form = ReviewForm(request.POST)
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.movie_id = concert_id
    new_review.save()
  return redirect('detail', concert_id=concert_id)

@login_required
def assoc_review(request, concert_id, review_id):
  Concert.objects.get(id=concert_id).reviews.add(review_id)
  return redirect('detail', concert_id=concert_id)


class ReviewList(LoginRequiredMixin, ListView):
  model = Review

class ReviewDetail(LoginRequiredMixin, DetailView):
  model = Review

class ReviewCreate(LoginRequiredMixin, CreateView):
  model = Review
  fields = '__all__'

class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  fields = '__all__'

class ReviewDelete(LoginRequiredMixin, DeleteView):
  model = Review
  success_url = '/reviews/'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_photo(request, concert_id):
    S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
    BUCKET = 'pyvengersunit3'
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, concert_id=concert_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', concert_id=concert_id)