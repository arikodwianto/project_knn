from django import forms
from .models import DataUji

class DataUjiForm(forms.ModelForm):
    class Meta:
        model = DataUji
        exclude = ['hasil_prediksi']

from django import forms
from .models import DataLatih

class DataLatihForm(forms.ModelForm):
    class Meta:
        model = DataLatih
        fields = ['nama', 'hari', 'waktu', 'durasi', 'paket', 'status']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrasiForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Alamat Email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nama Pengguna'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kata Sandi'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ulangi Kata Sandi'
        })
