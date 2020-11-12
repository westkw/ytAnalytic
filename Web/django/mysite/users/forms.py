from django import forms
from django.contrib.auth.models import User
from .models import Channel

class UserSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['channel_id']