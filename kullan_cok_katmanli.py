import cok_katmanli

# Nesneyi oluştur
ag = cok_katmanli.cok_katmanli_ag(ogrenme_katsayisi=0.5, momentum_katsayisi=0.2, katman_sayisi=3, ornek_sayisi=2)

# Ağırlık ve biasları oluştur
agirlik_tensoru, bias_vektoru = ag.agirlik_vektoru_olustur(katman_sayisi=ag.katman_sayisi, ornek_sayisi=ag.ornek_sayisi)

# Örnek giriş ve çıkış verileri
girdi_vektoru = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

# Burada örnek olarak XOR problemi için çıkışlar
cikti_vektoru = [0, 1, 1, 0]

# Boyut bilgisini al
boyut_bilgisi = ag.tensorun_boyutunu_al(agirlik_tensoru)

# Eğitimi başlat (epoch sayısı 1000 olsun)
ag.egitim(epoch_sayisi=100, girdi_vektoru=girdi_vektoru, cikti_vektoru=cikti_vektoru,
          agirlik_tensoru=agirlik_tensoru, bias_vektoru=bias_vektoru, boyut_bilgisi=boyut_bilgisi)

# Test et
print("\nTest Sonuçları:")
ag.test_et(girdi_vektoru, boyut_bilgisi, agirlik_tensoru, bias_vektoru)
