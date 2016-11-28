from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
# from . import models
from .models import Users
from .models import Quotes

import datetime

# Create your views here.

def index(request):
    return redirect('/main')

def main(request):
    return render(request,'pythontest/index.html')

def quotes(request):
    id=Users.objects.get(id=request.session['user_id'])
    context={
    'first_name':Users.objects.filter(id=request.session['user_id'])[0].first_name,
    'quotes':Quotes.objects.all().exclude(favorite=id),
    'favorites':Quotes.objects.all().filter(favorite=id)
    }
    return render(request,'pythontest/quotes.html',context)

def regprocess(request):
    form=request.POST
    response=Users.objects.registration(form)
    print Users.objects.all()
    if not response[0]:
        for error in response[1]:
            messages.add_message(request,messages.INFO,error )
        return redirect('/')
    else:
        id=Users.objects.filter(email=request.POST['email'])[0].id
        request.session['user_id']=id
        return redirect('/quotes')

def loginprocess(request):
    form = request.POST
    response=Users.objects.login(form)
    if not response[0]:
        for error in response[1]:
            messages.add_message(request,messages.INFO,error)
        return redirect('/')
    else:
        id=Users.objects.filter(email=request.POST['email'])[0].id
        request.session['user_id']=id
        return redirect('/quotes')


def add(request):
    id=Users.objects.get(id=request.session['user_id'])
    form=request.POST
    response=Users.objects.add(form,id)
    if not response[0]:
        for error in response[1]:
            messages.add_message(request,messages.INFO,error)
        return redirect('/quotes')
    else:
        return redirect('/quotes')

def add_list(request,id):
    user=Users.objects.get(id=request.session['user_id'])
    quote=Quotes.objects.get(id=id)
    quote.favorite.add(user)
    return redirect('/quotes')

def remove(request, id):
    user=Users.objects.get(id=request.session['user_id'])
    quote=Quotes.objects.get(id=id)
    quote.favorite.remove(user)
    return redirect('/quotes')

def user(request,id):
    user=Users.objects.get(id=id)
    context={
    'user':user,
    'quotes':Quotes.objects.filter(creator=id)
    }
    return render(request,'pythontest/user.html',context)

def logout(request):
    request.session.pop('user_id')
    return redirect('/')
