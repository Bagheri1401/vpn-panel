from django.db import models
from django.utils import timezone
from datetime import timedelta

class Server(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    ssh_port = models.IntegerField(default=22)
    ssh_user = models.CharField(max_length=100)
    ssh_key_path = models.CharField(max_length=255)

class Package(models.Model):
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField()
    traffic_limit_mb = models.BigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class VPNUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    protocol = models.CharField(max_length=20, choices=[('v2ray','V2Ray'), ('openvpn','OpenVPN'), ('l2tp','L2TP')])
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    traffic_used_mb = models.BigIntegerField(default=0)

    def renew(self):
        self.expire_at = timezone.now() + timedelta(days=self.package.duration_days)
        self.save()

class Reseller(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=64, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
