from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ChoirMember

class ChoirMemberRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)  # Make email optional
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    voice_part = forms.ChoiceField(choices=ChoirMember.VOICE_PARTS, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')  # Handle empty email
        if commit:
            user.save()
            ChoirMember.objects.create(
                user=user,
                voice_part=self.cleaned_data.get('voice_part'),
                phone_number=self.cleaned_data.get('phone_number', ''),
            )
        return user

# Add this class after ChoirMemberRegistrationForm
class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = ChoirMember
        fields = ['voice_part', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        choir_member = super().save(commit=False)
        if commit:
            # Update User model fields
            user = choir_member.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            choir_member.save()
        return choir_member 