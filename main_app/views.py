from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #this is a class and therefore using upper camel casing

import uuid
import boto3
from .models import Concert, Photo

class ConcertCreate(LoginRequiredMixin, CreateView):
  model = Concert
  fields = ['artist', 'location', 'date', 'time']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user #form.instance is the concert
    # Let the CreateView do its job as usual
    return super().form_valid(form)

# class ConcertUpdate(LoginRequiredMixin, UpdateView):
#   model = Concert
#   fields = ['artist', 'date', 'location']

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'pyvengersunit3'

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def concerts_index(request):
  concerts = Concert.objects.filter(user=request.user)
  return render(request, 'concerts/index.html', { 'concerts' : concerts })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, cat_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, cat_id=cat_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', cat_id=cat_id)