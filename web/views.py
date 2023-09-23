from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Kategori, Status
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
import requests
import hashlib
import datetime
import random


def index(request):
    return render(request, 'index.html')

def get_data(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    offset = (int(page) - 1) * int(per_page)

    products = Product.objects.raw('''
        SELECT p.id, p.nama_produk, p.harga, k.nama_kategori, s.nama_status, k.id as kat_id, s.id as sta_id
        FROM web_product p
        JOIN web_kategori k ON p.kategori_id = k.id
        JOIN web_status s ON p.status_id = s.id
        WHERE s.nama_status = 'bisa dijual'
        ORDER BY p.id
        LIMIT %s OFFSET %s
    ''', [per_page, offset])

    total_items = Product.objects.filter(status__nama_status='bisa dijual').count()
    total_pages = (total_items + int(per_page) - 1) // int(per_page)

    get_sta = Status.objects.all()
    get_kat = Kategori.objects.all()

    return JsonResponse({
        'data': [{'id': p.id, 'nama_produk': p.nama_produk, 'harga': p.harga, 'nama_kategori': p.nama_kategori, 'nama_status': p.nama_status, 'kat_id': p.kat_id, 'sta_id': p.sta_id} for p in products],
        'current_page': int(page),
        'per_page': int(per_page),
        'total_pages': total_pages,
        'total_items': total_items,
        'getsta': [{'id': s.id, 'nama_status': s.nama_status} for s in get_sta],
        'getkat': [{'id': k.id, 'nama_kategori': k.nama_kategori} for k in get_kat]
    })

@csrf_exempt
def call_api(request):
    waktu_sekarang = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    waktu_ditambah_1_jam = waktu_sekarang + datetime.timedelta(hours=1)
    tanggal_dmy = waktu_ditambah_1_jam.strftime('%d%m%y')
    jam = waktu_ditambah_1_jam.strftime('%H')

    username = f'tesprogrammer{tanggal_dmy}C{jam}'

    tanggal_sekarang = waktu_sekarang.strftime('%d-%m-%y')
    password = f'bisacoding-{tanggal_sekarang}'

    data = {
        'username': username,
        'password': hashlib.md5(password.encode()).hexdigest()
    }

    url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    response = requests.post(url, data=data)
    api_response = response.json()

    if api_response['error'] == 0:
        count = insert_data_from_api(api_response['data'])
        return JsonResponse({'status': 0, 'count': count})
    else:
        return JsonResponse({'status': 1})

def insert_data_from_api(api_response):
    count = 0
    for val in api_response:
        kategori, created = Kategori.objects.get_or_create(nama_kategori=val['kategori'])
        status, created = Status.objects.get_or_create(nama_status=val['status'])

        product, created = Product.objects.get_or_create(
            id=val['id_produk'],
            defaults={
                'nama_produk': val['nama_produk'],
                'harga': val['harga'],
                'kategori_id': kategori.id,
                'status_id': status.id
            }
        )

        if created:
            count += 1

    return count

@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            harga = form.cleaned_data['harga']
            kategori = form.cleaned_data['ketegori']
            status = form.cleaned_data['status']

            Product.objects.create(
                nama_produk=product,
                harga=harga,
                kategori=kategori,
                status=status
            )

            return JsonResponse({'status': 1,'message': 'Data berhasil disimpan'})
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] 
            return JsonResponse({'status': 0, 'message': errors})

@csrf_exempt
def edit_data(request, id):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = request.POST.get('product')
            harga = request.POST.get('harga')
            ketegori = request.POST.get('ketegori')
            status = request.POST.get('status')

            if product and harga and ketegori and status:
                kategori = Kategori.objects.get(id=ketegori)
                status = Status.objects.get(id=status)

                Product.objects.filter(id=id).update(
                    nama_produk=product,
                    harga=harga,
                    kategori=kategori,
                    status=status
                )

            return JsonResponse({'status': 1,'message': 'Data berhasil disimpan'})
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] 
            return JsonResponse({'status': 0, 'message': errors})

@csrf_exempt
def hapus_data(request, id):
    if request.method == 'POST':
        Product.objects.filter(id=id).delete()
        return JsonResponse({'message': 'Data berhasil dihapus'})

