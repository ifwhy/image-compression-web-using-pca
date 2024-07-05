from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from . import compress_pca
import time
import os

dummy = ""

def index(request):
    if request.method == 'POST' and 'photo' in request.FILES:
        image = request.FILES['photo']
        compress_percentage = int(request.POST['compress_percentage'])

        if not (1 <= compress_percentage <= 100):
            return HttpResponse("Tingkat kompresi harus antara 1 dan 100.")

        # Simpan file sementara
        fs = FileSystemStorage(location='static/img-compress/before')
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)
        temp_path = fs.path(filename)
        
        try:
            # Ukur waktu kompresi
            start_time = time.time()

            # Kompres gambar
            compressed_img = compress_pca.compress_image(temp_path, compress_percentage)

            end_time = time.time()
            compression_time = end_time - start_time

            # Simpan hasil kompresi
            compressed_filename = f'compressed_{filename}'
            compressed_path = os.path.join('static/img-compress/after', compressed_filename)
            compressed_img.save(compressed_path)

            # Setting presisi 2 desimal di belakang koma untuk waktu kompresi
            precision = 2
            compression_time = round(compression_time, precision)
            
            file_url = "static/img-compress/before/" + filename
            
            # Cari ukuran data asli dan hasil kompresi
            original_size = os.path.getsize(file_url)
            compressed_img_size = os.path.getsize(compressed_path)
            diff_size = abs(original_size - compressed_img_size)
            
            # Kirim Data Hasil
            context = {
                'original_image_url': file_url,
                'compressed_image_url': compressed_path,
                'compression_time': compression_time,
                'compress_percentage': compress_percentage,
                'compress_difference': diff_size
            }
            
            global dummy 
            dummy = compressed_path
            return render(request, 'result.html', context)

        except Exception as e:
            # Penanganan error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return HttpResponse(f"Terjadi kesalahan: {str(e)}")

    return render(request, 'index.html')

def download(request):
    compressed_image_path = dummy
    if os.path.exists(compressed_image_path):
        return FileResponse(open(compressed_image_path, 'rb'), as_attachment=True)
    else:
        return HttpResponse("File tidak ditemukan.")
