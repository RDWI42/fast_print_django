from django import forms
from .models import Kategori, Status
from django.core.validators import MinValueValidator

class ProductForm(forms.Form):
    product = forms.CharField(max_length=100, error_messages={
        'required': 'Nama Produk harus diisi'
    })
    harga = forms.DecimalField(validators=[MinValueValidator(0.01)], error_messages={
        'required': 'Harga harus diisi',
        'min_value': 'Harga harus bernilai lebih dari 0',
        'invalid': 'Harga harus berupa angka'
    })
    ketegori = forms.ModelChoiceField(queryset=Kategori.objects.all(), error_messages={
        'required': 'Kategori harus diisi'
    })
    status = forms.ModelChoiceField(queryset=Status.objects.all(), error_messages={
        'required': 'Status harus diisi'
    })
