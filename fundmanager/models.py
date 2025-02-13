from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)  # Automatically set the payment date

    def __str__(self):
        return f"Payment for {self.event.name} by {self.student.username}"
    
    def save(self, *args, **kwargs):
        print(self.event.fund_collected, self.amount_paid)
        self.event.fund_collected += self.amount_paid
        self.event.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        print(self)
        print(self.event.fund_collected, self.amount_paid)
        print("Delete overriden")
        self.event.fund_collected = self.event.fund_collected - self.amount_paid
        self.event.save()
        
        super().delete(*args, **kwargs)

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Branch name (e.g., CSE, ECE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    admission_number = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    batch = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username  # Or any other meaningful representation

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=200, blank=True)
    participants = models.IntegerField(blank=True)
    fund_required = models.DecimalField(max_digits=10, decimal_places=2)
    fund_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Initialize to 0
    fund_per_person = models.DecimalField(max_digits=6, decimal_places=2)
    batches = models.CharField(max_length=200, help_text="Comma-separated list of batches (e.g., 2020, 2021, 2022)")
    branches = models.ManyToManyField(Branch, related_name='events', help_text="Branches invited to the event", blank=True)
    coordinator1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_managing1', default=0)
    coordinator1_phone = models.CharField(max_length=20, blank=True)
    coordinator2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_managing2', default=0)
    coordinator2_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"