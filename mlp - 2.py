import random

# Girdiler ve istenen çıktılar
girdi_vektoru = [[0, 1, 2], [1, 2, 4], [5, 6, 8]]
cikti_vektoru = [1, 0, 0]

# Sabitler
e = 2.71828
son_bias = 0.14
ogrenme_katsayisi = 0.3
momentum_katsayisi = 0.2



def sigmoid_fonksiyonu(girdi):
    return 1 / (1 + pow(e, -girdi))


def tensorun_boyutunu_al(tensor):
    boyut = 0
    boyut_bilgisi = []
    while isinstance(tensor, list):
        boyut += 1
        boyut_bilgisi.append([boyut, len(tensor)])
        if len(tensor) == 0:
            break
        tensor = tensor[0]
    return boyut_bilgisi


def agirlik_vektoru_olustur(baslangic_degeri=0.0, degisim=1.0, katman_sayisi=4, ornek_sayisi=3):
    agirlik_tensoru = []
    bias_vektoru = []
    for _ in range(katman_sayisi):
        katman = []
        bias_katmani = []
        for _ in range(ornek_sayisi):
            noron_agirliklari = []
            for _ in range(ornek_sayisi):
                noron_agirliklari.append(random.uniform(baslangic_degeri, baslangic_degeri + degisim))
            katman.append(noron_agirliklari)
            bias_katmani.append(random.uniform(baslangic_degeri, baslangic_degeri + degisim))
        agirlik_tensoru.append(katman)
        bias_vektoru.append(bias_katmani)
    return agirlik_tensoru, bias_vektoru


# Ağırlık ve bias oluştur
agirlik_tensoru, bias_vektoru = agirlik_vektoru_olustur()
boyut_bilgisi = tensorun_boyutunu_al(agirlik_tensoru)

print("Başlangıç ağırlıkları:")
print(agirlik_tensoru)
print("Başlangıç bias:")
print(bias_vektoru)

# Her örnek için işlem yap
for ornek_i in range(len(girdi_vektoru)):
    deger_list = []

    for k_s in range(boyut_bilgisi[0][1]):  # Katman
        katman_cikti = []
        for o_s in range(boyut_bilgisi[1][1]):  # Nöron

            toplam = 0
            for g_s in range(boyut_bilgisi[2][1]):  # Girişler

                if k_s == 0:
                    girdi = girdi_vektoru[ornek_i][g_s]
                else:
                    deger_index = (k_s - 1) * boyut_bilgisi[1][1] + g_s
                    if deger_index < len(deger_list):
                        girdi = deger_list[deger_index]
                    else:
                        girdi = 0

                toplam += agirlik_tensoru[k_s][o_s][g_s] * girdi

            toplam += bias_vektoru[k_s][o_s]
            cikti = sigmoid_fonksiyonu(toplam)
            katman_cikti.append(cikti)
        deger_list.extend(katman_cikti)

    # Son çıkışı hesapla (output layer sonrası)
    son_list = deger_list[-len(girdi_vektoru[0]):]
    son_agirlik_list = agirlik_tensoru[-1][-1][-3:]  # son nöronun ağırlıkları

    toplam_son = 0
    for a in range(len(son_list)):
        toplam_son += son_list[a] * son_agirlik_list[a]

    son_deger = toplam_son + son_bias
    cikti = sigmoid_fonksiyonu(son_deger)

    hata = cikti * (1 - cikti) * (cikti_vektoru[ornek_i] - cikti)

    print(f"\nGirdi {ornek_i + 1}:")
    print("Çıktı:", cikti)
    print("Hata:", hata)

    # Ağırlık güncelle (output ağırlıkları)
    for a in range(len(son_list)):
        agirlik_degisimi = ogrenme_katsayisi * hata * son_list[a] + momentum_katsayisi * son_list[a]
        agirlik_tensoru[-1][-1][a] += agirlik_degisimi

    # Bias güncelle (son katman son nöronu)
    bias_vektoru[-1][-1] += ogrenme_katsayisi * hata

    # Ağırlık tensorünü güncelle (tüm katmanlar için)
    flat_index = 0
    for k_s in range(boyut_bilgisi[0][1]):
        for o_s in range(boyut_bilgisi[1][1]):
            for g_s in range(boyut_bilgisi[2][1]):
                if flat_index < len(deger_list):
                    d = deger_list[flat_index]
                    agirlik_degisimi = ogrenme_katsayisi * hata * d + momentum_katsayisi * d
                    agirlik_tensoru[k_s][o_s][g_s] += agirlik_degisimi

                    # Bias güncelle
                    bias_vektoru[k_s][o_s] += ogrenme_katsayisi * hata

                    flat_index += 1

print("\nGüncellenmiş ağırlık tensorü:")
print(agirlik_tensoru)

agirlik_tensoru, bias_vektoru = agirlik_vektoru_olustur()
boyut_bilgisi = tensorun_boyutunu_al(agirlik_tensoru)


def egitim(girdi_vektoru, agirlik_tensoru, bias_vektoru, boyut_bilgisi):
    
    for ornek_i in range(len(girdi_vektoru)):
        deger_list = []

        for k_s in range(boyut_bilgisi[0][1]):  # Katman
            katman_cikti = []
            for o_s in range(boyut_bilgisi[1][1]):  # Nöron

                toplam = 0
                for g_s in range(boyut_bilgisi[2][1]):  # Girişler

                    if k_s == 0:
                        girdi = girdi_vektoru[ornek_i][g_s]
                    else:
                        deger_index = (k_s - 1) * boyut_bilgisi[1][1] + g_s
                        if deger_index < len(deger_list):
                            girdi = deger_list[deger_index]
                        else:
                            girdi = 0

                    toplam += agirlik_tensoru[k_s][o_s][g_s] * girdi

                toplam += bias_vektoru[k_s][o_s]
                cikti = sigmoid_fonksiyonu(toplam)
                katman_cikti.append(cikti)
            deger_list.extend(katman_cikti)

    # Son çıkışı hesapla (output layer sonrası)
    son_list = deger_list[-len(girdi_vektoru[0]):]
    son_agirlik_list = agirlik_tensoru[-1][-1][-3:]  # son nöronun ağırlıkları

    toplam_son = 0
    for a in range(len(son_list)):
        toplam_son += son_list[a] * son_agirlik_list[a]

    son_deger = toplam_son + son_bias
    cikti = sigmoid_fonksiyonu(son_deger)

    hata = cikti * (1 - cikti) * (cikti_vektoru[ornek_i] - cikti)

    print(f"\nGirdi {ornek_i + 1}:")
    print("Çıktı:", cikti)
    print("Hata:", hata)

    # Ağırlık güncelle (output ağırlıkları)
    for a in range(len(son_list)):
        agirlik_degisimi = ogrenme_katsayisi * hata * son_list[a] + momentum_katsayisi * son_list[a]
        agirlik_tensoru[-1][-1][a] += agirlik_degisimi

    # Bias güncelle (son katman son nöronu)
    bias_vektoru[-1][-1] += ogrenme_katsayisi * hata

    # Ağırlık tensorünü güncelle (tüm katmanlar için)
    flat_index = 0
    for k_s in range(boyut_bilgisi[0][1]):
        for o_s in range(boyut_bilgisi[1][1]):
            for g_s in range(boyut_bilgisi[2][1]):
                if flat_index < len(deger_list):
                    d = deger_list[flat_index]
                    agirlik_degisimi = ogrenme_katsayisi * hata * d + momentum_katsayisi * d
                    agirlik_tensoru[k_s][o_s][g_s] += agirlik_degisimi

                    # Bias güncelle
                    bias_vektoru[k_s][o_s] += ogrenme_katsayisi * hata

                    flat_index += 1




test_girdi = [1, 2, 3]



def test_et(girdi):
    print("\n--- TEST ---")
    test_girdi = [1, 2, 3]
    test_deger_list = []

    for k_s in range(boyut_bilgisi[0][1]):
        katman_cikti = []
        for o_s in range(boyut_bilgisi[1][1]):
            toplam = 0
            for g_s in range(boyut_bilgisi[2][1]):
                if k_s == 0:
                    girdi = test_girdi[g_s]
                else:
                    deger_index = (k_s - 1) * boyut_bilgisi[1][1] + g_s
                    if deger_index < len(test_deger_list):
                        girdi = test_deger_list[deger_index]
                    else:
                        girdi = 0
                toplam += agirlik_tensoru[k_s][o_s][g_s] * girdi
            toplam += bias_vektoru[k_s][o_s]
            cikti = sigmoid_fonksiyonu(toplam)
            katman_cikti.append(cikti)
        test_deger_list.extend(katman_cikti)

    # Çıkış katmanı
    son_list = test_deger_list[-len(test_girdi):]
    son_agirlik_list = agirlik_tensoru[-1][-1][-3:]

    toplam_son = 0
    for a in range(len(son_list)):
        toplam_son += son_list[a] * son_agirlik_list[a]

    son_deger = toplam_son + son_bias
    test_cikti = sigmoid_fonksiyonu(son_deger)

    print("Test girdisi:", test_girdi)
    print("Ağın çıktısı:", test_cikti)

test_et(test_girdi)