from django import forms
from .models import Event, Payment

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'date',
            'participants',
            'fund_required',
            'fund_per_person',
            'batches',
            'branches',
            'coordinator1',
            'coordinator2',
        ]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["event", "student", "amount_paid"]