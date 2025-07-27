from django.shortcuts import render, redirect
from .models import VPNUser, Server, Package, Reseller
from django.utils import timezone
from django import forms
from uuid import uuid4
from .tasks import create_v2ray_user
from .forms import VPNUserForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def dashboard(request):
    users = VPNUser.objects.all()
    return render(request, 'dashboard.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = VPNUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.expire_at = timezone.now() + timezone.timedelta(days=user.package.duration_days)
            user.save()
            if user.protocol == 'v2ray':
                uuid = str(uuid4())
                result = create_v2ray_user(user.server, user.username, uuid)
            return redirect('dashboard')
    else:
        form = VPNUserForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
def reseller_dashboard(request):
    if not hasattr(request.user, 'reseller'):
        return JsonResponse({'error': 'Access denied'}, status=403)
    users = VPNUser.objects.all()
    return render(request, 'reseller_dashboard.html', {'users': users})

def update_traffic(username, amount_mb):
    try:
        user = VPNUser.objects.get(username=username)
        user.traffic_used_mb += amount_mb
        user.save()
    except VPNUser.DoesNotExist:
        pass

def auto_renew_expiring_accounts():
    now = timezone.now()
    for user in VPNUser.objects.filter(is_active=True, expire_at__lte=now):
        user.renew()
