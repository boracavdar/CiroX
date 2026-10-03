import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="CiroX Karar Motoru", layout="wide")
DB_YOLU = "gastro.db"

def getir_veri(sorgu):
    with sqlite3.connect(DB_YOLU) as conn:
        return pd.read_sql_query(sorgu, conn)

st.title("CiroX Finansal Karar Motoru")
st.markdown("---")

# --- GEÇMİŞ VERİ VE HESAPLAMALAR ---
df_gecmis = getir_veri("SELECT date, (cash_t + card_t) as ciro FROM daily_closing")
df_gecmis['date'] = pd.to_datetime(df_gecmis['date'])
df_gecmis['gun_index'] = df_gecmis['date'].dt.weekday

# Gelecek tahmini için haftanın günlerine göre son 3 ayın ortalamasını alıyoruz
son_3_ay = df_gecmis[df_gecmis['date'] > (pd.Timestamp.now() - pd.DateOffset(months=3))]
gunluk_ortalamalar = son_3_ay.groupby('gun_index')['ciro'].mean().to_dict()

# --- TAHMİN KONTROL PANELİ ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("⚙️ Projeksiyon Ayarı")
    secenekler = {"1 Haftalık (7 Gün)": 7, "2 Haftalık (14 Gün)": 14, "1 Aylık (30 Gün)": 30}
    secim = st.selectbox("Tahmin Süresi Seçin:", list(secenekler.keys()))
    gun_sayisi = secenekler[secim]
    
    # Bugünün cirosu (Ekranda dolgu olsun diye dün olarak alıyoruz)
    bugun_ciro = float(df_gecmis.iloc[-1]['ciro']) if not df_gecmis.empty else 0
    st.metric(label="Son Kapanış (Dikiz Aynası)", value=f"{bugun_ciro:,.0f} TL")

with col2:
    st.subheader(f"📈 Gelecek {gun_sayisi} Günün Kestirimci (Predictive) Trendi")
    
    bugun = datetime.now()
    gelecek_tarihler = []
    tahmin_cirolar = []

    for i in range(1, gun_sayisi + 1):
        gelecek_gun = bugun + timedelta(days=i)
        gelecek_tarihler.append(gelecek_gun.strftime("%Y-%m-%d"))
        # İlgili günün geçmiş ortalamasını bul
        tahmin = gunluk_ortalamalar.get(gelecek_gun.weekday(), 0)
        tahmin_cirolar.append(tahmin)

    df_tahmin = pd.DataFrame({"Tarih": pd.to_datetime(gelecek_tarihler), "Beklenen Ciro (TL)": tahmin_cirolar})
    df_tahmin.set_index("Tarih", inplace=True)
    
    # Grafiği çizdir (Streamlit'in şık native grafiği)
    st.line_chart(df_tahmin, use_container_width=True, color="#fbbf24")