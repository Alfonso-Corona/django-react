from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records

# Create your views here.
def home(request):
  records = Records.objects.all()

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    print(username, password)
    user = authenticate(request, username=username, password=password)
    print(user)

    if user is not None:
      login(request, user)
      messages.success(request, 'You have successfully logged in!')
      return redirect('home')
    else:
      messages.error(request, 'Error logging in. Please try again.')
      return redirect('home')
  else:
    return render(request, 'home.html', {
      'records': records
    })

def login_user(request):
  pass

def logout_user(request):
  logout(request)
  messages.success(request, 'You have successfully logged out!')
  return redirect('home')

def register_user(request):
  if(request.method == 'POST'):
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']

      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, 'You have successfully registered!')
      return redirect('home')
  else:
    form = SignUpForm()
    return render(request, 'register.html', {
      'form': form
    })
  return render(request, 'register.html', {
    'form': form
  })

def customer_record(request, pk):
  if request.user.is_authenticated:
    customer_record = Records.objects.get(id=pk)
    return render(request, 'record.html', {
      'customer_record': customer_record
    })
  else:
    messages.error(request, 'You must be logged in to view this page.')
    return redirect('home')
  
def delete_record(request, pk):
  if request.user.is_authenticated:
    delete_it = Records.objects.get(id=pk)
    delete_it.delete()
    messages.error(request, 'Record has been deleted.')
    return redirect('home')
  else:
    messages.error(request, 'You must be logged in to delete a record.')
    return redirect('home')
  
def add_record(request):
  form = AddRecordForm(request.POST or None)
  if request.user.is_authenticated:
    if request.method == 'POST':
      if form.is_valid():
        add_record = form.save()
        messages.success(request, 'Record has been added!')
        return redirect('home') 
    return render(request, 'add_record.html', {
      'form': form
    })
  else:
    messages.error(request, 'You must be logged in to add a record.')
    return redirect('home')
  
def update_record(request, pk):
  if request.user.is_authenticated:
    customer_record = Records.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=customer_record)
    if form.is_valid():
      form.save()
      messages.success(request, 'Record has been updated!')
      return redirect('home') 
    return render(request, 'update_record.html', {
      'form': form
    })
  else:
    messages.error(request, 'You must be logged in to update a record.')
    return redirect('home')