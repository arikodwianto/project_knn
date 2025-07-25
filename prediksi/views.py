from django.shortcuts import render
from .models import DataLatih, DataUji
from .forms import DataUjiForm
import math
from django.shortcuts import render, redirect  # ← tambahkan redirect


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

from .models import DataLatih
from math import sqrt

from django.shortcuts import render
from .forms import DataUjiForm
from .models import DataLatih
from collections import Counter
from sklearn.preprocessing import LabelEncoder
import numpy as np

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

# View untuk registrasi
from .forms import RegistrasiForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrasiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasi berhasil, silakan login.')
            return redirect('login')
    else:
        form = RegistrasiForm()
    return render(request, 'prediksi/register.html', {'form': form})

# View untuk login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()
    return render(request, 'prediksi/login.html', {'form': form})

# View untuk logout
def logout_view(request):
    logout(request)
    return redirect('login')


def prediksi_knn(data_uji, k=3):
    data_latih = DataLatih.objects.all()
    if not data_latih:
        return "Tidak Ada Data Latih", []

    # Encoder
    le_hari = LabelEncoder()
    le_waktu = LabelEncoder()
    le_paket = LabelEncoder()

    hari_list = [d.hari for d in data_latih]
    waktu_list = [d.waktu for d in data_latih]
    paket_list = [d.paket for d in data_latih]

    le_hari.fit(hari_list)
    le_waktu.fit(waktu_list)
    le_paket.fit(paket_list)

    # Data latih numerik
    X = []
    y = []

    for data in data_latih:
        fitur = [
            le_hari.transform([data.hari])[0],
            le_waktu.transform([data.waktu])[0],
            data.durasi,
            le_paket.transform([data.paket])[0],
        ]
        X.append(fitur)
        y.append(data.status)

    # Data uji numerik
    data_uji_fitur = [
        le_hari.transform([data_uji.hari])[0],
        le_waktu.transform([data_uji.waktu])[0],
        data_uji.durasi,
        le_paket.transform([data_uji.paket])[0],
    ]

    # Hitung jarak
    jarak = []
    for i, x in enumerate(X):
        dist = np.linalg.norm(np.array(x) - np.array(data_uji_fitur))
        jarak.append((dist, y[i], data_latih[i].nama))  # tambahkan nama biar informatif

    jarak.sort()
    k_terdekat = jarak[:k]

    status_terbanyak = Counter([s for _, s, _ in k_terdekat]).most_common(1)[0][0]
    return status_terbanyak, k_terdekat

@login_required
def index(request):
    form = DataUjiForm(request.POST or None)
    hasil = None
    perhitungan = []

    if form.is_valid():
        data_uji = form.save(commit=False)
        hasil, perhitungan = prediksi_knn(data_uji)
        data_uji.hasil_prediksi = hasil
        data_uji.save()

    return render(request, 'prediksi/index.html', {
        'form': form,
        'hasil': hasil,
        'perhitungan': perhitungan,
    })




from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import DataUjiForm, DataLatihForm
from .models import DataLatih

import csv
import io
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import DataLatihForm, UploadFileForm
from .models import DataLatih

@login_required
def tambah_data_latih(request):
    form = DataLatihForm()
    upload_form = UploadFileForm()

    if request.method == 'POST':
        if 'submit_manual' in request.POST:
            form = DataLatihForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Data berhasil ditambahkan!")
                return redirect('tambah_data_latih')

        elif 'submit_upload' in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = request.FILES['file']
                try:
                    if file.name.endswith('.csv'):
                        decoded_file = file.read().decode('utf-8')
                        io_string = io.StringIO(decoded_file)
                        reader = csv.reader(io_string)
                        next(reader)  # skip header
                        for row in reader:
                            DataLatih.objects.create(
                                nama=row[0],
                                hari=int(row[1]),
                                waktu=int(row[2]),
                                durasi=int(row[3]),
                                paket=int(row[4]),
                                status=row[5]
                            )
                    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                        df = pd.read_excel(file)
                        for _, row in df.iterrows():
                            DataLatih.objects.create(
                                nama=row['nama'],
                                hari=int(row['hari']),
                                waktu=int(row['waktu']),
                                durasi=int(row['durasi']),
                                paket=int(row['paket']),
                                status=row['status']
                            )
                    else:
                        messages.error(request, "❌ Format file tidak didukung.")
                        return redirect('tambah_data_latih')

                    messages.success(request, "✅ File berhasil diimport!")
                    return redirect('tambah_data_latih')

                except Exception as e:
                    messages.error(request, f"❌ Gagal mengimport: {e}")

    data_latih = DataLatih.objects.all()
    return render(request, 'prediksi/tambah_data_latih.html', {
        'form': form,
        'upload_form': upload_form,
        'data_latih': data_latih
    })


