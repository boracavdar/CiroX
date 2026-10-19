import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CiroX Yapay Zeka", layout="wide")
st.title("🧠 CiroX - AI Karar Destek Sistemi")
st.markdown("Balık sezonu dinamiklerine göre Günlük, Haftalık ve Aylık ciro projeksiyonları.")
st.markdown("---")

model_yolu = 'cirox_beyin.pkl'
if os.path.exists(model_yolu):
    model = joblib.load(model_yolu)
    
    # Arayüzü Sekmelere (Tab) bölüyoruz
    tab1, tab2 = st.tabs(["📅 Tek Günlük Tahmin", "📊 Haftalık / Aylık Projeksiyon"])
    
    with tab1:
        st.subheader("Yarın İçin Detaylı Simülasyon")
        col1, col2 = st.columns(2)
        with col1:
            hava_sicakligi = st.slider("Hava Sıcaklığı (°C)", -5, 45, 10, key="gunluk_isi")
            yagis_var_mi = st.checkbox("🌧️ Yağmur veya Kar Bekleniyor mu?", key="gunluk_yagis")
        with col2:
            haftasonu_mu = st.checkbox("📅 Yarın Hafta Sonu mu?", key="gunluk_haftasonu")
            mac_var_mi = st.checkbox("⚽ Maç/Etkinlik Var mı?", key="gunluk_mac")
            ozel_gun_mu = st.checkbox("🎉 Özel Gün mü?", key="gunluk_ozel")

        if st.button("🔮 Günlük Tahmin Et", type="primary", use_container_width=True):
            veri = pd.DataFrame({'hava_sicakligi': [hava_sicakligi], 'yagis_var_mi': [1 if yagis_var_mi else 0], 
                                 'haftasonu_mu': [1 if haftasonu_mu else 0], 'ozel_gun_mu': [1 if ozel_gun_mu else 0], 
                                 'mac_var_mi': [1 if mac_var_mi else 0]})
            sonuc = model.predict(veri)[0]
            st.success(f"### 🎯 Beklenen Günlük Ciro: {sonuc:,.0f} TL")

    with tab2:
        st.subheader("Gelecek Projeksiyonu (Otomatik Takvim)")
        st.info("Sistem bugünden itibaren ileriye dönük takvimi tarar ve hafta sonlarını (Cuma, Cmt, Pzr) otomatik tespit eder.")
        
        periyot = st.radio("Hesaplanacak Dönem:", ["7 Günlük (Haftalık Bilanço)", "30 Günlük (Aylık Bilanço)"])
        gun_sayisi = 7 if periyot == "7 Günlük (Haftalık Bilanço)" else 30
        
        col3, col4 = st.columns(2)
        with col3:
            ort_sicaklik = st.slider(f"Bu {gun_sayisi} gün için Ortalama Sıcaklık (°C)", -5, 45, 8, key="periyot_isi")
            yagisli_gun_sayisi = st.number_input(f"Kaç gün yağışlı/karlı geçer?", min_value=0, max_value=gun_sayisi, value=2)
        with col4:
            mac_gunu_sayisi = st.number_input(f"Dönem içinde kaç maç/etkinlik günü var?", min_value=0, max_value=gun_sayisi, value=1)
            ozel_gun_sayisi = st.number_input(f"Kaç tane özel gün (Bayram, Tatil vb.) var?", min_value=0, max_value=gun_sayisi, value=0)
        
        if st.button("🚀 Projeksiyonu Başlat", type="primary", use_container_width=True):
            tahminler = []
            tarihler = []
            bugun = datetime.now()
            
            # Olayları günlere rastgele ama istenilen sayıda dağıtmak için listeler hazırlıyoruz
            yagis_listesi = [1]*int(yagisli_gun_sayisi) + [0]*(gun_sayisi - int(yagisli_gun_sayisi))
            mac_listesi = [1]*int(mac_gunu_sayisi) + [0]*(gun_sayisi - int(mac_gunu_sayisi))
            ozel_listesi = [1]*int(ozel_gun_sayisi) + [0]*(gun_sayisi - int(ozel_gun_sayisi))
            
            random.shuffle(yagis_listesi)
            random.shuffle(mac_listesi)
            random.shuffle(ozel_listesi)
            
            for i in range(gun_sayisi):
                gelecek_tarih = bugun + timedelta(days=i+1)
                tarihler.append(gelecek_tarih.strftime("%d %b")) # Örn: 04 Eki
                
                # Haftasonu kontrolü: 4(Cuma), 5(Cmt), 6(Pzr)
                is_weekend = 1 if gelecek_tarih.weekday() >= 4 else 0 
                
                gunluk_df = pd.DataFrame({
                    'hava_sicakligi': [ort_sicaklik],
                    'yagis_var_mi': [yagis_listesi[i]],
                    'haftasonu_mu': [is_weekend],
                    'ozel_gun_mu': [ozel_listesi[i]],
                    'mac_var_mi': [mac_listesi[i]]
                })
                
                gunluk_ciro = model.predict(gunluk_df)[0]
                tahminler.append(gunluk_ciro)
            
            toplam_ciro = sum(tahminler)
            
            st.success(f"### 💰 {gun_sayisi} Günlük Beklenen Toplam Ciro: {toplam_ciro:,.0f} TL")
            
            # Şık bir Ciro Dağılım Grafiği
            df_grafik = pd.DataFrame({"Tarih": tarihler, "Beklenen Ciro (TL)": tahminler})
            st.line_chart(df_grafik.set_index("Tarih"))

else:
    st.error("Model bulunamadı! Lütfen önce yapay zekayı eğitin.")