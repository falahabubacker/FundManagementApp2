from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Event, Payment, Branch, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import EventCreationForm, PaymentForm
from datetime import date
from django.contrib.auth import get_user_model
import re
from django.db.models import Q

User = get_user_model()

def redirect_home(request):
    return redirect('home')

def home(request):
    if request.user.is_authenticated == False: return redirect('signin')
    
    filtered_events = Event.objects.filter((Q(branches__in=[request.user.profile.department]) & Q(batches__contains=str(request.user.profile.batch))) |
                                           (Q(coordinator1=request.user.id) | Q(coordinator2=request.user.id))).distinct()
    return render(request, 'index.html', context={"events": filtered_events, "today": date.today()})

def signin(request):
    if request.user.is_authenticated == True: logout(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def event_details(request, id):
    if request.user.is_authenticated == False: return redirect('signin')
    event = get_object_or_404(Event, pk=id)
    if request.method == 'POST':

        for student_id in request.POST.getlist('paid_students'):
            save_form = PaymentForm({'event': id,
                                    'student': student_id,
                                    'amount_paid': event.fund_per_person})

            if save_form.is_valid():
                print("saved")
                save_form.save()  # Save the new payment to the database
            
        delete_payments = Payment.objects.filter(student__pk__in=request.POST.getlist('unpaid_students'))
        
        if delete_payments:
            for payment in delete_payments:
                payment.delete()  # Delete the unpaid payments from the database
    
        return redirect('event_details', id=id)
        
        
    
    paid_students = Payment.objects.filter(event=event).select_related('student')

    # Extract the students who paid
    paid_student_ids = [payment.student.id for payment in paid_students]

    # Get the list of invited branches for the event
    invited_branches = event.branches.all()
    invited_batches = event.batches.split(',')

    # Get all students who belong to the invited branches
    eligible_students = User.objects.filter(
        profile__department__in=invited_branches,
        profile__batch__in=invited_batches
    )

    # Filter out students who have already paid
    unpaid_students = [student for student in eligible_students if student.id not in paid_student_ids]

    context = {
        'event': event,
        'paid_students': paid_students,
        'unpaid_students': unpaid_students,
    }

    return render(request, 'event-details.html', context=context)

def create_event(request, id=None):
    if request.user.is_authenticated == False: return redirect('signin')
    if request.method == 'POST':
        
        if id:
            form = EventCreationForm(request.POST, instance=get_object_or_404(Event, id=id))
        else:
            form = EventCreationForm(request.POST)

        if form.is_valid():
            print('valid')
            form.save()  # Save the new event to the database
            return redirect('event_details', id=form.instance.id)  # Redirect to a list of events or a success page
        else:
            print(form['date'].value)
            context = {'form': form, 'users': UserProfile.objects.all()} # Pass the form with errors back to template
            return render(request, 'create-event.html', context) # Re-render with errors
    else:
        print('get')
        if id != None:
            form = EventCreationForm(instance=get_object_or_404(Event, id=id))
            print("Date:", form.instance.date)
            context = {'form': form, 'users': UserProfile.objects.all()} # Create context for the form
            return render(request, 'create-event.html', context)
        else:
            form = EventCreationForm()  # Create a blank form
            context = {'form': form, 'users': UserProfile.objects.all()} # Create context for the form
            return render(request, 'create-event.html', context)