import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Patron Ekranı", layout="wide")

# Sadece vitrin klasöründeki sahte veritabanına bakar
DB_YOLU = "gastro.db"

def getir_veri(sorgu, parametreler=()):
    if not os.path.exists(DB_YOLU):
        return pd.DataFrame()
    with sqlite3.connect(DB_YOLU) as conn:
        return pd.read_sql_query(sorgu, conn, params=parametreler)

bugun = datetime.now()
yarin = bugun + timedelta(days=1)
bugun_str = bugun.strftime("%Y-%m-%d")

gun_isimleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
yarin_isim = gun_isimleri[yarin.weekday()]
yarin_gun_index = yarin.weekday()

# --- DİKİZ AYNASI (BUGÜN) ---
# Simülasyon olduğu için bugünü boş göstermemek adına dünün verisini alıyoruz
dun_str = (bugun - timedelta(days=1)).strftime("%Y-%m-%d")
sorgu_bugun = "SELECT (cash_t + card_t + cash_k + card_k) as ciro FROM daily_closing WHERE date = ?"
df_bugun = getir_veri(sorgu_bugun, (dun_str,))
bugun_ciro = float(df_bugun['ciro'].iloc[0]) if not df_bugun.empty else 0.0

# --- UZUN FAR (YARIN TAHMİNİ) ---
df_gecmis = getir_veri("SELECT date, (cash_t + card_t + cash_k + card_k) as ciro FROM daily_closing WHERE (cash_t + card_t + cash_k + card_k) > 0")

tahmini_ciro = 0.0
benzer_gun_sayisi = 0

if not df_gecmis.empty:
    df_gecmis['date'] = pd.to_datetime(df_gecmis['date'])
    df_gecmis['gun_index'] = df_gecmis['date'].dt.weekday
    hedef_gunler = df_gecmis[df_gecmis['gun_index'] == yarin_gun_index]
    benzer_gun_sayisi = len(hedef_gunler)
    
    if benzer_gun_sayisi > 0:
        tahmini_ciro = float(hedef_gunler['ciro'].mean())

# --- TASARIM ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 style='text-align: center; color: #94a3b8; margin-bottom: 20px;'>DİKİZ AYNASI (BUGÜN)</h2>", unsafe_allow_html=True)
    html_sol = f"""
    <div style='background-color: #064e3b; padding: 80px 20px; border-radius: 20px; text-align: center; color: white;'>
        <p style='font-size: 80px; margin: 0; font-weight: 900;'>{bugun_ciro:,.0f} TL</p>
        <p style='font-size: 24px; margin: 10px 0 0 0; color: #cbd5e1;'>Şu Ana Kadar Kasaya Giren</p>
    </div>
    """
    st.markdown(html_sol, unsafe_allow_html=True)

with col2:
    st.markdown(f"<h2 style='text-align: center; color: #fbbf24; margin-bottom: 20px;'>UZUN FAR (YARIN: {yarin_isim.upper()})</h2>", unsafe_allow_html=True)
    html_sag = f"""
    <div style='background-color: #1e3a8a; padding: 80px 20px; border-radius: 20px; text-align: center; color: white;'>
        <p style='font-size: 80px; margin: 0; font-weight: 900;'>~ {tahmini_ciro:,.0f} TL</p>
        <p style='font-size: 24px; margin: 10px 0 0 0; color: #bfdbfe;'>Geçmiş {benzer_gun_sayisi} {yarin_isim} ortalaması</p>
    </div>
    """
    st.markdown(html_sag, unsafe_allow_html=True)