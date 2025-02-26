from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ChoirMember

class ChoirMemberRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    voice_part = forms.ChoiceField(choices=ChoirMember.VOICE_PARTS, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        ChoirMember.objects.create(
            user=user,
            voice_part=self.cleaned_data.get('voice_part'),
            phone_number=self.cleaned_data.get('phone_number', ''),
            profile_picture=self.cleaned_data.get('profile_picture'),
        )
        return user

class ChoirMemberProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = ChoirMember
        fields = ['voice_part', 'phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        choir_member = super().save(commit=False)
        if commit:
            # Update User model fields
            user = choir_member.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            choir_member.save()
        return choir_member