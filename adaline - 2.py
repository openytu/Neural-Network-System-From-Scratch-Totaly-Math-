girdi_vektoru = [[0,1], [1,2], [5,6], [9,2]]

cikti_vektoru = [1, 0, 0, 1]

agirlik_vektoru = [0.2, 0.5, 0.3, 0.7]

ogrenme_katsayisi = 0.01

bias = 0.1

parca_uzunlugu = len(girdi_vektoru[0])

agirliklandirilmis_vektor = []

tekrar = 16

for t in range(tekrar):

    [agirliklandirilmis_vektor.append(d[j] * agirlik_vektoru[j]) for i, d in enumerate(girdi_vektoru) for j in range(len(girdi_vektoru[0]))]

    print(agirliklandirilmis_vektor)


    [i for i, d in enumerate(agirliklandirilmis_vektor)]

    agirliklandirilmis_vektor_duzenli = []


    for i in range((parca_uzunlugu * 4)):
        if i % 2 == 0:
            agirliklandirilmis_vektor_duzenli.append(agirliklandirilmis_vektor[i:i+2])


    print(agirliklandirilmis_vektor_duzenli)

    toplanmis_vektor = [sum(i) + bias for i in agirliklandirilmis_vektor_duzenli]

    print(toplanmis_vektor)

    for i, d in enumerate(toplanmis_vektor):
        if (d < 2 and cikti_vektoru[i] == 1) or (d > 2 and cikti_vektoru[i] == 0):
            hata = cikti_vektoru[i] - d
            print("hata:", hata)
            for j in range(parca_uzunlugu):
                print(i, j)
                agirlik_vektoru[i] = agirlik_vektoru[i] + ogrenme_katsayisi * hata * girdi_vektoru[i][j]
                bias = bias + ogrenme_katsayisi * hata

print(agirlik_vektoru)

