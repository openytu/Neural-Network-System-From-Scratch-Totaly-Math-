import random

class cok_katmanli_ag:
    def __init__(self, e = 2, ogrenme_katsayisi = .5, momentum_katsayisi = .2, katman_sayisi=4, ornek_sayisi=3, son_bias = 0.14):
        self.katman_sayisi = katman_sayisi
        self.ornek_sayisi = ornek_sayisi
        self.ogrenme_katsayisi = ogrenme_katsayisi      
        self.momentum_katsayisi = momentum_katsayisi    
        self.agirliklar = []
        self.biaslar = []
        self.e = 2.71828
        self.son_bias = son_bias
        self.onceki_agirlik_degisimleri = None  # Önceki ağırlık değişimleri burada saklanacak
    

    def tensorun_boyutunu_al(self, tensor):
        boyut = 0
        boyut_bilgisi = []
        while isinstance(tensor, list):
            boyut += 1
            boyut_bilgisi.append([boyut, len(tensor)])
            if len(tensor) == 0:
                break
            tensor = tensor[0]
        return boyut_bilgisi
    
    def agirlik_vektoru_olustur(self, baslangic_degeri=0.0, degisim=1.0, katman_sayisi=4, ornek_sayisi=3):
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
        
        # Önceki ağırlık değişimleri sıfırlarla aynı boyutta oluşturuluyor
        self.onceki_agirlik_degisimleri = []
        for katman in agirlik_tensoru:
            katman_degisim = []
            for noron in katman:
                noron_degisim = [0.0 for _ in noron]
                katman_degisim.append(noron_degisim)
            self.onceki_agirlik_degisimleri.append(katman_degisim)
        
        return agirlik_tensoru, bias_vektoru


    def sigmoid_fonksiyonu(self, girdi):
        return 1 / (1 + pow(self.e, -girdi))
    
    def egitim(self, epoch_sayisi:int, girdi_vektoru:list, cikti_vektoru:list, agirlik_tensoru:list, bias_vektoru:list, boyut_bilgisi:list):
    
        for x in range(epoch_sayisi):
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
                        cikti = self.sigmoid_fonksiyonu(toplam)
                        katman_cikti.append(cikti)
                    deger_list.extend(katman_cikti)

            # Son çıkışı hesapla (output layer sonrası)
            son_list = deger_list[-len(girdi_vektoru[0]):]
            son_agirlik_list = agirlik_tensoru[-1][-1][-len(girdi_vektoru[0]):] # son nöronun ağırlıkları

            

            toplam_son = 0
            for a in range(len(son_list)):
                toplam_son += son_list[a] * son_agirlik_list[a]

            son_deger = toplam_son + self.son_bias
            cikti = self.sigmoid_fonksiyonu(son_deger)

            hata = cikti * (1 - cikti) * (cikti_vektoru[ornek_i] - cikti)

            print(f"\nGirdi {ornek_i + 1}:")
            print("Çıktı:", cikti)
            print("Hata:", hata)

            # Ağırlık güncelle (output ağırlıkları)
            for a in range(len(son_list)):
                onceki_delta = self.onceki_agirlik_degisimleri[-1][-1][a]
                agirlik_degisimi = (self.ogrenme_katsayisi * hata * son_list[a]) + (self.momentum_katsayisi * onceki_delta)
                agirlik_tensoru[-1][-1][a] += agirlik_degisimi
                self.onceki_agirlik_degisimleri[-1][-1][a] = agirlik_degisimi

            # Bias güncelle (son katman son nöronu)
            bias_vektoru[-1][-1] += self.ogrenme_katsayisi * hata

            # Ağırlık tensorünü güncelle (tüm katmanlar için)
            flat_index = 0
            for k_s in range(boyut_bilgisi[0][1]):
                for o_s in range(boyut_bilgisi[1][1]):
                    for g_s in range(boyut_bilgisi[2][1]):
                        if flat_index < len(deger_list):
                            d = deger_list[flat_index]
                            onceki_delta = self.onceki_agirlik_degisimleri[k_s][o_s][g_s]
                            agirlik_degisimi = (self.ogrenme_katsayisi * hata * d) + (self.momentum_katsayisi * onceki_delta)
                            agirlik_tensoru[k_s][o_s][g_s] += agirlik_degisimi
                            self.onceki_agirlik_degisimleri[k_s][o_s][g_s] = agirlik_degisimi

                            # Bias güncelle
                            bias_vektoru[k_s][o_s] += self.ogrenme_katsayisi * hata

                            flat_index += 1


    def test_et(self, girdi, boyut_bilgisi, agirlik_tensoru, bias_vektoru):
        print("\n--- TEST ---")
        test_girdi = girdi  # Test verisini al
        test_deger_list = []  # Bu liste katmanların çıktıları için tutulacak

        # Her örnek için test yap
        for ornek_i in range(len(test_girdi)):  # Her örneği ayrı ayrı test et
            print(f"\nTest Örneği {ornek_i + 1}:")
            
            test_deger_list.clear()  # Her örnek için çıktı listesini temizle

            # Her katman için hesaplamalar
            for k_s in range(len(boyut_bilgisi) - 1):  # Son katman dışında tüm katmanlar
                katman_cikti = []  # Bu katmanın çıktılarını saklamak için
                for o_s in range(boyut_bilgisi[k_s + 1][1]):  # Nöron sayısı
                    toplam = 0
                    for g_s in range(boyut_bilgisi[k_s][1]):  # Girişler
                        if k_s == 0:
                            # İlk katman için girdi değeri doğrudan test_girdi'den alınacak
                            if g_s < len(test_girdi[ornek_i]):  # Burada g_s'nin sınırları kontrol edilmeli
                                girdi_degeri = test_girdi[ornek_i][g_s]  # Test verisinin o örneğinden girdi alınır
                                print(f"Girdi Değeri (k_s={k_s}, o_s={o_s}, g_s={g_s}):", girdi_degeri)
                                toplam += agirlik_tensoru[k_s][o_s][g_s] * girdi_degeri
                            else:
                                print(f"Error: g_s={g_s} out of range for test_girdi[ornek_i]")
                                continue  # Eğer index dışıysa geçerli değeri almayı geç
                        else:
                            # Diğer katmanlar için önceki katmandan alınan çıktı
                            if g_s < len(test_deger_list):  # test_deger_list'in boyutunu kontrol et
                                girdi_degeri = test_deger_list[g_s]
                                print(f"Girdi Değeri (k_s={k_s}, o_s={o_s}, g_s={g_s}):", girdi_degeri)
                                toplam += agirlik_tensoru[k_s][o_s][g_s] * girdi_degeri
                            else:
                                print(f"Error: g_s={g_s} out of range for test_deger_list")
                                continue  # Eğer index dışıysa geçerli değeri almayı geç

                    # Bias'ı ekleme
                    toplam += bias_vektoru[k_s][o_s]

                    # Aktivasyon fonksiyonuna sokma
                    cikti = self.sigmoid_fonksiyonu(toplam)
                    katman_cikti.append(cikti)

                # Bu katmanın çıktıları bir sonraki katman için kullanılacak
                test_deger_list.extend(katman_cikti)

            # Çıkış katmanı
            son_list = test_deger_list[-len(test_girdi[ornek_i]):]  # Çıkış için son nöronların çıktılarını al
            son_agirlik_list = agirlik_tensoru[-1][-1][-len(test_girdi[ornek_i]):]  # Son katman için ağırlıkları al
            print("son_agirlik_list: ", son_agirlik_list)
            print("son_list: ", son_list)
            
            # Çıkış değeri hesaplama
            toplam_son = 0
            for a in range(len(son_list)):
                toplam_son += son_list[a] * son_agirlik_list[a]  # Sonuç için ağırlıklarla çarpma

            # Bias'ı ekleme
            son_deger = toplam_son + self.son_bias
            test_cikti = self.sigmoid_fonksiyonu(son_deger)  # Sigmoid fonksiyonu ile sonucu hesapla

            print("Test girdisi:", test_girdi[ornek_i])
            print("Ağın çıktısı:", test_cikti)
