import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# 1. Eğitim Verisini Veritabanından Çek
conn = sqlite3.connect("gastro.db")
df = pd.read_sql_query("SELECT * FROM ml_daily_closing", conn)
conn.close()

# 2. Özellikler (X) ve Hedef (y) Olarak Ayır
# Tarih sütununu atıyoruz çünkü model metin değil, sayılardan anlar
X = df[['hava_sicakligi', 'yagis_var_mi', 'haftasonu_mu', 'ozel_gun_mu', 'mac_var_mi']]
y = df['ciro']

# 3. Veriyi Parçala: %80'i ile ders çalışacak, %20'si ile kendini test edecek
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Yapay Zeka geçmiş 1 yıllık veriyi inceliyor ve gizli örüntüleri öğreniyor...")

# 4. Modeli Kur ve Eğit
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Sınav Vakti (Test setindeki ciro rakamlarını tahmin etmeye çalışıyor)
tahminler = model.predict(X_test)
hata_payi = mean_absolute_error(y_test, tahminler)
basari_orani = r2_score(y_test, tahminler)

print("\n--- EĞİTİM SONUÇLARI ---")
print(f"📊 Ortalama Hata Payı: {hata_payi:,.0f} TL")
print(f"🎯 Modelin Başarı Oranı (Doğruluk): %{basari_orani*100:.1f}")

# 6. Öğrenen Beyni Kalıcı Olarak Kaydet
# (Böylece program her açıldığında tekrar eğitim yapmak zorunda kalmayacak)
joblib.dump(model, 'cirox_beyin.pkl')
print("\n✅ Eğitilmiş zeka 'cirox_beyin.pkl' dosyasına kaydedildi!")