import numpy as np
from PIL import Image
from sklearn.decomposition import PCA

def compress_image(image_path, compress_percentage):
    # Baca gambar
    img = Image.open(image_path)
    
    # Konversi ke array numpy
    img_array = np.array(img)
      
    # Pisahkan channel warna
    r = img_array[:, :, 0]
    g = img_array[:, :, 1]
    b = img_array[:, :, 2]
    
    # Fungsi untuk melakukan kompresi PCA pada channel warna
    def pca_compress(channel, compress_percentage):
        h, w = channel.shape
        n_components = int(min(h, w) * (compress_percentage / 100.0))
        pca = PCA(n_components=n_components)
        channel_compressed = pca.fit_transform(channel)
        channel_restored = pca.inverse_transform(channel_compressed)
        return channel_restored, n_components, pca.components_
    
    # Lakukan PCA untuk setiap channel
    r_restored, r_components, r_pca_components = pca_compress(r, compress_percentage)
    g_restored, g_components, g_pca_components = pca_compress(g, compress_percentage)
    b_restored, b_components, b_pca_components = pca_compress(b, compress_percentage)
    
    # Gabungkan kembali channel warna dan klip ke rentang yang benar
    restored_img = np.dstack((r_restored, g_restored, b_restored))
    restored_img = np.clip(restored_img, 0, 255).astype(np.uint8)
    
    # Buat gambar PIL dari array
    restored_pil = Image.fromarray(restored_img)
    
    return restored_pil