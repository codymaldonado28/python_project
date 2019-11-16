from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'E-Mail or Password is incorrect')
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/profile')
        else:
            messages.error(request, 'E-Mail or Password is incorrect')
            return redirect('/')

    return redirect('/')


def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=pw_hash
            )
            request.session['user_id'] = User.objects.last().id

    return redirect('/')


def profile(request):
    if not 'id' in request.session:
        messages.error(request, "must log in")
        return redirect('/')
    creator_trip = Trip.objects.filter(
        creator=User.objects.get(id=request.session['id']))
    my_trips = Trip.objects.filter(
        users=User.objects.get(id=request.session['id']))
    others_trip = my_trips.exclude(
        creator=User.objects.get(id=request.session['id']))
    trip = Trip.objects.exclude(
        users=User.objects.get(id=request.session['id']))
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
        'trips': trip,
        'creator_trip': creator_trip,
        'others_trip': others_trip,
    }
    return render(request, 'profile.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def add_trip(request):
    return render(request, 'add_trip.html')


def create_trip(request):
    if request.method == "POST":
        try: 
            datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        except:
            messages.error(request,'worng end date format')
            return redirect('/trip/add')
        else:
            try: 
                datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            except:
                messages.error(request,'worng start date format')
                return redirect('/trip/add')
            else:
                errors = Trip.objects.basic_validator(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                        return redirect('/trip/add')
                else:
                    trip = Trip.objects.create(
                        destination=request.POST['destination'],
                        start_date=request.POST['start_date'],
                        end_date=request.POST['end_date'],
                        plan=request.POST['plan'],
                        creator=User.objects.get(id=request.session['id'])
                    )
                    trip.users.add(User.objects.get(id=request.session['id'])) 
    return redirect('/profile')


def edit_trip_create(request, trip_id):
    if request.method == "POST":
        try: 
            datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        except:
            messages.error(request,'worng end date format')
            return redirect(f'/trip/edit[{trip_id}]')
        else:
            try: 
                datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            except:
                messages.error(request,'worng start date format')
                return redirect(f'/trip/edit/{trip_id}')
            else:
                errors = Trip.objects.basic_validator(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                        return redirect(f'/trip/edit/{trip_id}')
                else:
                    trip = Trip.objects.get(id=trip_id)
                    trip.destination = request.POST['destination']
                    trip.start_date = request.POST['start_date']
                    trip.end_date = request.POST['end_date']
                    trip.plan = request.POST['plan']
                    trip.save()
        return redirect('/profile')


def edit_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip': trip
    }
    return render(request, 'edit_trip.html', context)


def view_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip': trip
    }
    return render(request, 'view_trip.html', context)


def join_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.users.add(User.objects.get(id=request.session['id']))
    trip.save()
    return redirect('/profile')


def cancel_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.users = trip.users.exclude(id=request.session['id'])
    trip.save()
    return redirect('/profile')


def trip_delete(request, trip_id):
    print(trip_id)
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/profile')
