from django.shortcuts import render, redirect
from .models import VPNUser, Server, Package
from django.utils import timezone
from django import forms
from uuid import uuid4
from .tasks import create_v2ray_user

class VPNUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    protocol = forms.ChoiceField(choices=[('v2ray','V2Ray'), ('openvpn','OpenVPN'), ('l2tp','L2TP')])
    server = forms.ModelChoiceField(queryset=Server.objects.all())
    package = forms.ModelChoiceField(queryset=Package.objects.all())

def dashboard(request):
    users = VPNUser.objects.all()
    return render(request, 'dashboard.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = VPNUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            expire_at = timezone.now() + timezone.timedelta(days=data['package'].duration_days)
            user = VPNUser.objects.create(
                username=data['username'],
                password=data['password'],
                protocol=data['protocol'],
                server=data['server'],
                package=data['package'],
                expire_at=expire_at
            )
            if user.protocol == 'v2ray':
                uuid = str(uuid4())
                result = create_v2ray_user(user.server, user.username, uuid)
            return redirect('dashboard')
    else:
        form = VPNUserForm()
    return render(request, 'create_user.html', {'form': form})
