girdi_vektor = [[2, 3], [4, 5], [8, 12]]

cikti_vektor = [0, 1, 1]

esik_deger = -1

agirliklar = [0.7, 0.5]

ogrenme_katsayisi = 0.4

# e_number = 2.718281828459045

# def sigmoid_fonksiyonu(girdi):
#     1 / (1+ pow(e_number, -girdi))

def deneme(agirlik = [], girdi = [], esik = -1, y1= []):
    for i in range(len(girdi)):   
        toplam = girdi[i] * agirliklar[j]
        print(toplam)
        if (toplam > esik and y1[i] == 0) or (toplam < esik and y1[i] == 1):
            print("Tahmin doğru")
        
        else:
            print("Tahmin yanliş")


for i in range(len(girdi_vektor)):
    for j in range(len(girdi_vektor[0])):
        toplam = girdi_vektor[i][j] * agirliklar[j]
        # print(toplam)
    
    if (toplam > esik_deger and cikti_vektor[i] == 0) or (toplam < esik_deger and cikti_vektor[i] == 1):
        for a in range(len(agirliklar)):
            agirliklar[a] = agirliklar[a] - ogrenme_katsayisi * girdi_vektor[i][a]

    

print("Eğitilmiş Ağirliklar: ", agirliklar)

deneme(agirlik=agirliklar, girdi= [2, 0.1], esik=-1, y1 = [0, 0])




