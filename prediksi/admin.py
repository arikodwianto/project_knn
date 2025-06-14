# prediksi/admin.py
from django.contrib import admin
from .models import DataLatih, DataUji

admin.site.register(DataLatih)
admin.site.register(DataUji)
