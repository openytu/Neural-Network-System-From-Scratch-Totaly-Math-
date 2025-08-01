girdi_vektoru = [[0,1], [1,2], [5,6], [9,2]]

cikti_vektoru = [1, 0, 0, 1]

agirlik_vektoru = [[0.2, 0.5, -0.3, 0.6],
                   [-0.1, 0.2, 0.2, -0.3],
                   [0.2, -0.5, 0.1, 0.2]]

ogrenme_katsayisi = 0.2

bias = 0.1

tekrar = 20

for t in range(tekrar):
    for k in range(len(agirlik_vektoru)):
        toplam = 0
        for i in range(len(girdi_vektoru)):
            for j in range(len(girdi_vektoru[0])):
                    toplam = girdi_vektoru[i][j] * agirlik_vektoru[k][i]
        toplam = toplam + bias

        for a in range(len(cikti_vektoru)):
            if (toplam < 2 and cikti_vektoru[a] == 1) or (toplam > 2 and cikti_vektoru[a] == 0):
                hata = cikti_vektoru[a] - toplam
                print("hata:", hata)
                for j in range(len(girdi_vektoru[0])):
                    print(a, j)
                    agirlik_vektoru[k][a] = agirlik_vektoru[k][a] + ogrenme_katsayisi * hata * girdi_vektoru[a][j]
                    bias = bias + ogrenme_katsayisi * hata

print(agirlik_vektoru)