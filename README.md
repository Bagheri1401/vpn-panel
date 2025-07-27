# 🌐 VPN Control Panel

پنل تحت وب مدیریت اکانت‌های VPN (V2Ray، OpenVPN، L2TP) با Django  
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/bagheri1401/vpn-panel.svg?style=social)](https://github.com/bagheri1401/vpn-panel)

---

## ✨ ویژگی‌ها

- ساخت اکانت‌های V2Ray / OpenVPN / L2TP از طریق رابط تحت وب
- اتصال به چندین سرور مختلف
- تعریف پکیج (مدت‌زمان، حجم، قیمت)
- نمایش لیست کاربران و وضعیت مصرف
- پنل نمایندگی (با API Key)
- قابلیت تمدید خودکار بر اساس پکیج انتخاب‌شده
- پشتیبانی از نصب با Gunicorn + Nginx و فعال‌سازی HTTPS

---

## 📦 نصب سریع

```bash
sudo apt update && sudo apt install python3-pip python3-venv nginx git -y
cd /opt
git clone https://github.com/bagheri1401/vpn-panel.git
cd vpn-panel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

---

## 🚀 اجرای Gunicorn + Nginx

```bash
venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 vpn_panel.wsgi:application
```

### فایل سرویس systemd
```
/etc/systemd/system/vpn-panel.service
```

### پیکربندی دامنه با certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 📁 ساختار پروژه

- `models.py`: سرورها، کاربران، پکیج‌ها، نمایندگان
- `views.py`: داشبورد و فرم‌ها
- `tasks.py`: اجرای دستورات از راه دور
- `templates/`: رابط تحت وب ساده

---

## 📸 اسکرین‌شات‌ها

به‌زودی...

---

## 🧾 لایسنس

MIT © [bagheri1401](https://github.com/bagheri1401)
