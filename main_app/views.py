from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin #this is a class and therefore using upper camel casing

import uuid
import boto3
from .models import Concert

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

# class ConcertDelete(LoginRequiredMixin, DeleteView):
#   model = Concert
#   success_url = '/concerts/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def concerts_index(request):
  concerts = Concert.objects.filter(user=request.user)
  return render(request, 'concerts/index.html', { 'concerts' : concerts })

# @login_required
# def concerts_detail(request, concert_id):
# #   concerts = Concert.objects.get(id=concert_id)
#   return render(request, 'concerts/detail.html', { 'concert' : concert })

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