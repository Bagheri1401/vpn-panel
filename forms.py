from django import forms
from .models import VPNUser

class VPNUserForm(forms.ModelForm):
    class Meta:
        model = VPNUser
        fields = ['username', 'password', 'protocol', 'server', 'package']

    def clean_username(self):
        username = self.cleaned_data['username']
        if VPNUser.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً وجود دارد.")
        return username
