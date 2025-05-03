from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest, Bid, Review, Message, User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_resident = forms.BooleanField(required=False, initial=True)
    is_service_provider = forms.BooleanField(required=False, initial=False)
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_resident', 'is_service_provider',
                 'profile_picture', 'phone_number', 'address', 'bio']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'service_type', 'urgency', 'location']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'estimated_time', 'notes']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'phone_number', 'address', 'bio'] 