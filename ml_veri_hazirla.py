import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("gastro.db")
cursor = conn.cursor()

# Makine Öğrenmesi için zenginleştirilmiş yeni tablo
cursor.execute('''CREATE TABLE IF NOT EXISTS ml_daily_closing (
    date TEXT PRIMARY KEY, ciro REAL, hava_sicakligi INTEGER, 
    yagis_var_mi INTEGER, haftasonu_mu INTEGER, 
    ozel_gun_mu INTEGER, mac_var_mi INTEGER)''')

mevsim_carpanlari = {
    1: 1.8, 2: 1.7, 3: 1.3, 4: 1.1, 5: 0.9, 6: 0.6, 
    7: 0.5, 8: 0.6, 9: 0.9, 10: 1.2, 11: 1.5, 12: 1.9
}

bugun = datetime.now()
print("Yapay Zeka eğitim verisi üretiliyor (365 gün)...")

for i in range(1, 366):
    islem_tarihi = bugun - timedelta(days=i)
    ay = islem_tarihi.month
    
    # 1. Temel Özellikler
    haftasonu_mu = 1 if islem_tarihi.weekday() in [4, 5, 6] else 0
    ozel_gun_mu = 1 if random.random() < 0.03 else 0 # Yüzde 3 ihtimalle özel gün
    mac_var_mi = 1 if haftasonu_mu == 1 and random.random() < 0.2 else 0 # Hafta sonları %20 ihtimalle derbi
    
    # 2. Hava Durumu Kurgusu (Aya göre mantıklı sıcaklık ve yağış)
    if ay in [12, 1, 2]:    hava_sicakligi = random.randint(0, 12)
    elif ay in [6, 7, 8]:   hava_sicakligi = random.randint(25, 38)
    else:                   hava_sicakligi = random.randint(12, 24)
    
    # Kışın yağmur ihtimali yüksek, yazın düşük
    yagis_ihtimali = 0.4 if ay in [11, 12, 1, 2, 3] else 0.1
    yagis_var_mi = 1 if random.random() < yagis_ihtimali else 0
    
    # 3. Modelin Keşfedeceği Mantıksal Ciro Hesabı (Etki-Tepki)
    taban_ciro = random.uniform(15000, 20000)
    mevsim_etkisi = taban_ciro * mevsim_carpanlari[ay]
    
    # Dış etkenleri ciroya yansıtıyoruz (Model bu kuralları kendi öğrenecek)
    gercek_ciro = mevsim_etkisi
    if haftasonu_mu: gercek_ciro *= 1.5      # Hafta sonu %50 artar
    if yagis_var_mi: gercek_ciro *= 0.75     # Yağmur %25 düşürür
    if ozel_gun_mu:  gercek_ciro *= 1.8      # Özel gün %80 artırır
    if mac_var_mi:   gercek_ciro *= 1.3      # Maç günü %30 artırır
    
    # Veritabanına yaz
    cursor.execute('''INSERT OR REPLACE INTO ml_daily_closing 
                   (date, ciro, hava_sicakligi, yagis_var_mi, haftasonu_mu, ozel_gun_mu, mac_var_mi) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (islem_tarihi.strftime("%Y-%m-%d"), gercek_ciro, hava_sicakligi, 
                    yagis_var_mi, haftasonu_mu, ozel_gun_mu, mac_var_mi))

conn.commit()
conn.close()
print("✅ Zenginleştirilmiş ML veri seti başarıyla 'ml_daily_closing' tablosuna kaydedildi!")